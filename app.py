#!/usr/bin/env python3
import os
import sys
import subprocess
import logging
import re
import pytz
from zoneinfo import available_timezones

from flask import (
    Flask, render_template, request,
    flash, redirect, url_for, Response
)
from werkzeug.utils import secure_filename

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Map PyPI package → Django INSTALLED_APPS entry
APP_NAME_MAP = {
    "djangorestframework":  "rest_framework",
    "django-debug-toolbar": "debug_toolbar",
    "django-crispy-forms":  "crispy_forms",
    "django-allauth":       "allauth",
    "django-cors-headers":  "corsheaders",
    "django-environ":       None,
    "gunicorn":             None,
    "pytest":               None,
    "pytest-django":        None,
    "celery":               None,
    "channels":             "channels",
    "whitenoise":           "whitenoise.runserver_nostatic",
    "pillow":               None,
    "django-extensions":    "django_extensions",
    "django-filter":        "django_filters",
}

BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
PROJECTS_ROOT = os.path.join(BASE_DIR, "generated_projects")
os.makedirs(PROJECTS_ROOT, exist_ok=True)

SSE_HEADERS = {
    "Content-Type":      "text/event-stream",
    "Cache-Control":     "no-cache",
    "X-Accel-Buffering": "no"
}

def get_venv_bin_dir():
    return "Scripts" if os.name == "nt" else "bin"

def inject_manage_py_launcher(manage_py_path: str, bin_dir: str):
    python_exe_name = 'python.exe' if os.name == 'nt' else 'python'
    launcher = f"""# ── VENV LAUNCHER ──
import os, sys
_proj = os.path.dirname(os.path.abspath(__file__))
_venv_py = os.path.join(_proj, 'venv', '{bin_dir}', '{python_exe_name}')
if os.path.exists(_venv_py) and os.path.abspath(sys.executable) != os.path.abspath(_venv_py):
    os.execv(_venv_py, [_venv_py] + sys.argv)
# ────────────────────────

"""
    content = open(manage_py_path, 'r', encoding='utf-8').read()
    if "VENV LAUNCHER" not in content:
        with open(manage_py_path, 'w', encoding='utf-8') as f:
            f.write(launcher + content)
        try:
            os.chmod(manage_py_path, 0o755)
        except OSError:
            pass
        logger.info("Injected venv launcher into %s", manage_py_path)

def inject_venv_site_hack(settings_path: str):
    try:
        content = open(settings_path, 'r', encoding='utf-8').read()
    except FileNotFoundError:
        logger.error("settings.py not found at %s", settings_path)
        return

    hack = f"""# ── VENV SITE-PACKAGES HACK ──
import os, sys
_proj = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_venv = os.path.join(_proj, 'venv')
if os.name == 'nt':
    _lib = os.path.join('Scripts', 'Lib', 'site-packages')
else:
    _lib = os.path.join('lib', f"python{{sys.version_info.major}}.{{sys.version_info.minor}}", 'site-packages')
_site = os.path.join(_venv, _lib)
if os.path.isdir(_site) and _site not in sys.path:
    sys.path.insert(0, _site)
# ───────────────────────────────────

"""
    if "VENV SITE-PACKAGES HACK" not in content:
        with open(settings_path, 'w', encoding='utf-8') as f:
            f.write(hack + content)
        logger.info("Injected venv site-packages hack into %s", settings_path)

def inject_timezone(settings_path: str, timezone: str):
    """Insert or replace TIME_ZONE in settings.py, validate via zoneinfo."""
    if timezone not in available_timezones():
        logger.warning("Invalid TIME_ZONE '%s', falling back to UTC", timezone)
        timezone = 'UTC'

    try:
        content = open(settings_path, 'r', encoding='utf-8').read()
    except FileNotFoundError:
        logger.error("settings.py not found at %s", settings_path)
        return

    tz_line = f"TIME_ZONE = '{timezone}'"
    if re.search(r"^TIME_ZONE\s*=", content, re.MULTILINE):
        content = re.sub(r"^TIME_ZONE\s*=.*", tz_line, content, flags=re.MULTILINE)
    elif "USE_TZ = True" in content:
        content = content.replace("USE_TZ = True", tz_line + "\nUSE_TZ = True")
    else:
        content = tz_line + "\n" + content

    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(content)
    logger.info("Set TIME_ZONE to %s in %s", timezone, settings_path)

def inject_apps_into_settings(settings_path: str, apps: list):
    """Append missing apps to INSTALLED_APPS in settings.py."""
    try:
        content = open(settings_path, 'r', encoding='utf-8').read()
    except FileNotFoundError:
        logger.error("settings.py not found at %s", settings_path)
        return

    match = re.search(r"(INSTALLED_APPS\s*=\s*\[)(.*?)(\])", content, flags=re.DOTALL)
    if not match:
        logger.warning("INSTALLED_APPS not found in %s", settings_path)
        return

    pre, inner, post = match.groups()
    existing = {
        line.strip(" '\"\n,")
        for line in inner.splitlines()
        if line.strip().startswith(("'", '"'))
    }

    additions = [f"    '{app}',\n" for app in apps if app not in existing]
    if not additions:
        return

    new_inner   = inner + "".join(additions)
    new_block   = pre + new_inner + post
    new_content = content[:match.start()] + new_block + content[match.end():]

    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    logger.info("Injected %d app(s) into INSTALLED_APPS", len(additions))


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template(
        'index.html',
        packages=list(APP_NAME_MAP.keys()),
        timezones=sorted(available_timezones())
    )


@app.route('/stream_create')
def stream_create():
    # Gather & sanitize inputs
    raw_name      = request.args.get('project_name', '')
    project_name  = secure_filename(raw_name.strip())
    if not project_name:
        def err():
            yield "data: ❌ Numele proiectului nu poate fi gol sau invalid.\n\n"
            yield "event: done\ndata: error\n\n"
        return Response(err(), headers=SSE_HEADERS)

    install_django = request.args.get('install_django') == 'on'
    selected_pkgs  = [p for p in request.args.getlist('packages') if p in APP_NAME_MAP]
    tz             = request.args.get('timezone', 'UTC')

    raw_apps       = request.args.get('apps', '')
    user_apps      = [
        nm for nm in (
            secure_filename(x.strip()) for x in raw_apps.split(',')
        ) if nm and nm.isidentifier()
    ]

    # superuser creds (optional)
    su_username = request.args.get('su_username', '').strip()
    su_email    = request.args.get('su_email', '').strip()
    su_password = request.args.get('su_password', '').strip()

    # auto-enable Django if needed
    if (user_apps or su_username) and not install_django:
        install_django = True

    # Prepare paths & executables
    target_dir    = os.path.join(PROJECTS_ROOT, project_name)
    venv_dir      = os.path.join(target_dir, 'venv')
    bin_dir       = get_venv_bin_dir()
    python_exe    = os.path.join(venv_dir, bin_dir, 'python' + ('.exe' if os.name=='nt' else ''))
    pip_exe       = os.path.join(venv_dir, bin_dir, 'pip' + ('.exe' if os.name=='nt' else ''))
    django_admin  = os.path.join(venv_dir, bin_dir, 'django-admin' + ('.exe' if os.name=='nt' else ''))
    settings_rel  = os.path.join(project_name, 'settings.py')
    settings_path = os.path.join(target_dir, settings_rel)

    pip_pkgs = (['django'] if install_django else []) + selected_pkgs

    def generate():
        valid_third = []

        # Create project folder
        yield f"data: 📁 Creare folder `{project_name}`...\n\n"
        try:
            os.makedirs(target_dir, exist_ok=False)
            yield "data: ✔ Folder creat.\n\n"
        except Exception as e:
            yield f"data: ❌ Eroare la creare folder: {e}\n\n"
            yield "event: done\ndata: error\n\n"
            return

        # Create virtualenv
        yield "data: 🐍 Creare venv...\n\n"
        try:
            subprocess.check_call(
                [sys.executable, '-m', 'venv', venv_dir],
                stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
            )
            yield "data: ✔ venv creat.\n\n"
        except Exception as e:
            yield f"data: ❌ Eroare venv: {e}\n\n"
            yield "event: done\ndata: error\n\n"
            return

        # Install pip packages
        if pip_pkgs:
            yield f"data: 📦 Instalare pachete: {', '.join(pip_pkgs)}...\n\n"
            proc = subprocess.Popen(
                [pip_exe, 'install'] + pip_pkgs,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1
            )
            for line in proc.stdout:
                yield f"data: {line.rstrip()}\n\n"
            if proc.wait() != 0:
                yield f"data: ❌ pip install exit code {proc.returncode}\n\n"
                yield "event: done\ndata: error\n\n"
                return
            yield "data: ✔ Pachete instalate.\n\n"

            # Verify third-party modules
            yield "data: 🔍 Verificare module importabile…\n\n"
            for pkg in selected_pkgs:
                label = APP_NAME_MAP[pkg]
                if not label:
                    continue
                ok = subprocess.run(
                    [python_exe, '-c', f'import {label}'],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                ).returncode == 0
                if ok:
                    valid_third.append(label)
                    yield f"data: ✔ Modul '{label}' importabil.\n\n"
                else:
                    yield f"data: ⚠️ Modul '{label}' nu găsit; omis.\n\n"

        # Create & configure Django project
        if install_django:
            yield "data: 🔧 Creare proiect Django...\n\n"
            proc = subprocess.Popen(
                [django_admin, 'startproject', project_name, target_dir],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1
            )
            for line in proc.stdout:
                yield f"data: {line.rstrip()}\n\n"
            if proc.wait() != 0:
                yield f"data: ❌ django-admin exit code {proc.returncode}\n\n"
                yield "event: done\ndata: error\n\n"
                return
            yield "data: ✔ Proiect creat.\n\n"

            # Inject manage.py launcher
            manage_py = os.path.join(target_dir, 'manage.py')
            inject_manage_py_launcher(manage_py, bin_dir)
            yield "data: ✔ manage.py actualizat să folosească venv python\n\n"

            # Inject site-packages hack
            inject_venv_site_hack(settings_path)
            yield "data: ✔ Venv site-packages hack injectat în settings.py\n\n"

            # Ensure settings.py exists
            if not os.path.isfile(settings_path):
                yield f"data: ❌ Lipsește {settings_rel}\n\n"
                yield "event: done\ndata: error\n\n"
                return

            # Inject third-party apps
            if valid_third:
                yield "data: ✍️ Injectare third-party apps...\n\n"
                inject_apps_into_settings(settings_path, valid_third)
                yield "data: ✔ Third-party apps injectate.\n\n"

            # Inject timezone
            yield f"data: 🌐 Setare fus orar '{tz}'...\n\n"
            inject_timezone(settings_path, tz)
            yield "data: ✔ TIME_ZONE setat.\n\n"

            # Create user apps
            if user_apps:
                yield f"data: 📦 Creare apps: {', '.join(user_apps)}...\n\n"
                for nm in user_apps:
                    yield f"data: 🔍 Verific conflict pentru '{nm}'…\n\n"
                    if subprocess.run(
                        [python_exe, '-c', f'import {nm}'],
                        cwd=target_dir,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                    ).returncode == 0:
                        yield f"data: ⚠️ '{nm}' există ca modul; omis.\n\n"
                        continue

                    proc = subprocess.Popen(
                        [python_exe, os.path.join(target_dir, 'manage.py'), 'startapp', nm],
                        cwd=target_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                        text=True, bufsize=1
                    )
                    for line in proc.stdout:
                        yield f"data: {line.rstrip()}\n\n"
                    if proc.wait() != 0:
                        yield f"data: ⚠️ Creare app '{nm}' eșuat; omis.\n\n"
                        continue

                    yield f"data: ✔ App '{nm}' creat.\n\n"
                    yield f"data: ✍️ Injectare '{nm}' în INSTALLED_APPS...\n\n"
                    inject_apps_into_settings(settings_path, [nm])
                    yield f"data: ✔ '{nm}' adăugat.\n\n"

            # Generate helper scripts
            yield "data: ⚙️ Generare start.sh & start.bat...\n\n"
            start_sh = os.path.join(target_dir, 'start.sh')
            with open(start_sh, 'w', encoding='utf-8') as f:
                f.write(f"""#!/usr/bin/env bash
cd "$(dirname "$0")"
source venv/{bin_dir}/activate
python manage.py runserver
""")
            try: os.chmod(start_sh, 0o755)
            except OSError: pass

            start_bat = os.path.join(target_dir, 'start.bat')
            with open(start_bat, 'w', encoding='utf-8') as f:
                f.write(f"""@echo off
cd /d %~dp0
call venv\\{bin_dir}\\activate.bat
python manage.py runserver
""")
            yield "data: ✔ Helper scripts create.\n\n"

            # Apply migrations
            yield "data: 🚜 Aplicare migrări Django...\n\n"
            migrate_cmd = [
                python_exe,
                os.path.join(target_dir, 'manage.py'),
                'migrate'
            ]
            proc = subprocess.Popen(
                migrate_cmd,
                cwd=target_dir,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1
            )
            for line in proc.stdout:
                yield f"data: {line.rstrip()}\n\n"
            if proc.wait() != 0:
                yield f"data: ❌ migrate exit code {proc.returncode}\n\n"
                yield "event: done\ndata: error\n\n"
                return
            yield "data: ✔ Migrări aplicate.\n\n"

            # Create superuser (after migrations)
            if su_username:
                yield "data: 🚀 Creare superuser…\n\n"
                env = os.environ.copy()
                env.update({
                    'DJANGO_SUPERUSER_USERNAME': su_username,
                    'DJANGO_SUPERUSER_EMAIL':    su_email or 'admin@example.com',
                    'DJANGO_SUPERUSER_PASSWORD': su_password or 'admin',
                })
                cmd = [
                    python_exe,
                    os.path.join(target_dir, 'manage.py'),
                    'createsuperuser',
                    '--noinput'
                ]
                proc = subprocess.Popen(
                    cmd,
                    cwd=target_dir,
                    env=env,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, bufsize=1
                )
                for line in proc.stdout:
                    yield f"data: {line.rstrip()}\n\n"
                if proc.wait() != 0:
                    yield f"data: ❌ Superuser exit code {proc.returncode}\n\n"
                else:
                    yield "data: ✔ Superuser creat.\n\n"

        # final done
        yield "event: done\ndata: success\n\n"

    return Response(generate(), headers=SSE_HEADERS)


@app.route('/create_project', methods=['POST'])
def create_project():
    flash('Proiect creat (fallback).', 'success')
    return redirect(url_for('index'))


if __name__ == "__main__":
    # disable Flask’s reloader so SSE streams cleanly
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
