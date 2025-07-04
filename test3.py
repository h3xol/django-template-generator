#!/usr/bin/env python3
import os
import sys
import subprocess
import logging
import re
import pytz

from flask import (
    Flask, render_template, request,
    flash, redirect, url_for, Response
)
from werkzeug.utils import secure_filename

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------

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

# Place all generated Django projects here (so they're outside Flask's watch)
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
PROJECTS_ROOT = os.path.join(BASE_DIR, "generated_projects")
os.makedirs(PROJECTS_ROOT, exist_ok=True)

def get_venv_bin_dir():
    return "Scripts" if os.name == "nt" else "bin"

def inject_timezone(settings_path: str, timezone: str):
    """Insert or replace TIME_ZONE in settings.py."""
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()

    pat = re.compile(r"^TIME_ZONE\s*=\s*['\"].*?['\"]", re.MULTILINE)
    line = f"TIME_ZONE = '{timezone}'"
    if pat.search(content):
        content = pat.sub(line, content)
    else:
        content = content.replace(
            "USE_TZ = True",
            f"{line}\nUSE_TZ = True"
        )

    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(content)
    logger.info("Set TIME_ZONE to %s in %s", timezone, settings_path)

def inject_apps_into_settings(settings_path: str, apps: list):
    """Append missing apps to INSTALLED_APPS in settings.py."""
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()

    pat = re.compile(r"(INSTALLED_APPS\s*=\s*\[)(.*?)(\])", re.DOTALL)
    m = pat.search(content)
    if not m:
        logger.warning("INSTALLED_APPS not found in %s", settings_path)
        return

    pre, inner, post = m.groups()
    existing = {
        ln.strip(" '\"\n,")
        for ln in inner.splitlines()
        if ln.strip().startswith(("'", '"'))
    }

    additions = [f"    '{app}',\n" for app in apps if app not in existing]
    if not additions:
        return

    new_inner   = inner + "".join(additions)
    new_block   = pre + new_inner + post
    new_content = content[:m.start()] + new_block + content[m.end():]

    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    logger.info("Injected %d app(s) into INSTALLED_APPS", len(additions))

# ------------------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template(
        'index2.html',
        packages=list(APP_NAME_MAP.keys()),
        timezones=pytz.common_timezones
    )

@app.route('/stream_create')
def stream_create():
    # 1) Gather & sanitize inputs
    project_name   = secure_filename(request.args.get('project_name', '').strip())
    install_django = request.args.get('install_django') == 'on'
    selected_pkgs  = [
        p for p in request.args.getlist('packages')
        if p in APP_NAME_MAP
    ]

    tz = request.args.get('timezone', 'UTC')
    if tz not in pytz.common_timezones:
        tz = 'UTC'

    raw_apps = request.args.get('apps', '')
    user_apps = [
        secure_filename(a.strip()) for a in raw_apps.split(',') if a.strip()
    ]

    # 2) Prepare paths & commands
    target_dir    = os.path.join(PROJECTS_ROOT, project_name)
    venv_dir      = os.path.join(target_dir, 'venv')
    bin_dir       = get_venv_bin_dir()
    pip_pkgs      = (['django'] if install_django else []) + selected_pkgs
    pip_exe       = os.path.join(venv_dir, bin_dir, 'pip')
    python_exe    = os.path.join(venv_dir, bin_dir, 'python')
    django_admin  = os.path.join(venv_dir, bin_dir, 'django-admin')
    settings_path = os.path.join(target_dir, project_name, 'settings.py')
    third_party   = [
        APP_NAME_MAP[p] for p in selected_pkgs if APP_NAME_MAP[p]
    ]

    def generate():
        # 1) Create the project folder
        yield f"data: 📁 Creare folder `{project_name}`...\n\n"
        try:
            os.makedirs(target_dir, exist_ok=False)
            yield "data: ✔ Folder creat.\n\n"
        except Exception as e:
            yield f"data: ❌ Eroare la crearea folderului: {e}\n\n"
            yield "event: done\ndata: error\n\n"
            return

        # 2) Create virtualenv
        yield "data: 🐍 Creare venv...\n\n"
        try:
            subprocess.check_call([sys.executable, '-m', 'venv', venv_dir])
            yield "data: ✔ venv creat.\n\n"
        except Exception as e:
            yield f"data: ❌ Eroare venv: {e}\n\n"
            yield "event: done\ndata: error\n\n"
            return

        # 3) pip install packages
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
                yield f"data: ❌ Pip exit code {proc.returncode}\n\n"
                yield "event: done\ndata: error\n\n"
                return
            yield "data: ✔ Pachete instalate.\n\n"

        # 4) Django project + configuration
        if install_django:
            # a) django-admin startproject
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
            yield "data: ✔ Proiect Django creat.\n\n"

            # b) inject third-party apps
            if third_party:
                yield "data: ✍️ Injectare third-party apps...\n\n"
                inject_apps_into_settings(settings_path, third_party)
                yield "data: ✔ Third-party apps injectate.\n\n"

            # c) inject TIME_ZONE
            yield f"data: 🌐 Setare fus orar la '{tz}'...\n\n"
            inject_timezone(settings_path, tz)
            yield "data: ✔ TIME_ZONE setat.\n\n"

            # d) create user apps
            if user_apps:
                yield f"data: 📦 Creeare apps: {', '.join(user_apps)}...\n\n"
                for name in user_apps:
                    try:
                        proc = subprocess.Popen(
                            [python_exe, os.path.join(target_dir, 'manage.py'), 'startapp', name],
                            cwd=target_dir,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, bufsize=1
                        )
                    except Exception as e:
                        yield f"data: ❌ startapp {name} error: {e}\n\n"
                        yield "event: done\ndata: error\n\n"
                        return

                    for line in proc.stdout:
                        yield f"data: {line.rstrip()}\n\n"
                    if proc.wait() != 0:
                        yield f"data: ❌ startapp {name} failed (code {proc.returncode})\n\n"
                        yield "event: done\ndata: error\n\n"
                        return

                    yield f"data: ✔ App '{name}' creat.\n\n"
                    yield f"data: ✍️ Injectare '{name}' în INSTALLED_APPS...\n\n"
                    inject_apps_into_settings(settings_path, [name])
                    yield f"data: ✔ '{name}' adăugat.\n\n"

            # e) generate start.sh & start.bat
            yield "data: ⚙️ Generare start.sh & start.bat...\n\n"
            start_sh = os.path.join(target_dir, 'start.sh')
            with open(start_sh, 'w', encoding='utf-8') as f:
                f.write(f'''#!/usr/bin/env bash
cd "$(dirname "$0")"
source venv/{bin_dir}/activate
python manage.py runserver
''')
            try:
                os.chmod(start_sh, 0o755)
            except OSError:
                pass

            start_bat = os.path.join(target_dir, 'start.bat')
            with open(start_bat, 'w', encoding='utf-8') as f:
                f.write(f'''@echo off
cd /d %~dp0
call venv\\{bin_dir}\\activate.bat
python manage.py runserver
''')
            yield "data: ✔ Helper scripts create.\n\n"

        # 5) Done
        yield "event: done\ndata: success\n\n"

    headers = {
        "Content-Type":      "text/event-stream",
        "Cache-Control":     "no-cache",
        "X-Accel-Buffering": "no"
    }
    return Response(generate(), headers=headers)

@app.route('/create_project', methods=['POST'])
def create_project():
    # Fallback for non-JS clients
    flash('Proiect creat (fallback).', 'success')
    return redirect(url_for('index'))

# ------------------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    # disable Flask's reloader so SSE isn't cut mid-stream
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
