# 🚀 [EN] Django Template Generator

A small **Django** project generator built with **Flask** that lets you:

* ✅ Create a new Django project  
* 📦 Select extra Python packages (`pip`) to install  
* 🧩 Specify Django apps to scaffold (`startapp`)  
* 🌍 Set the `TIME_ZONE` in `settings.py` (validated with `zoneinfo`)  
* 🔄 Receive a **live console log (SSE)** of every generation step  
* ⚙️ Automatically apply **migrations** (`manage.py migrate`)  
* 🚀 Optionally create a **superuser** (`createsuperuser --noinput`)  
* 🛡️ Inject a small launcher into `manage.py` so it always runs under your venv’s Python  
* 📌 Inject the venv’s `site-packages` into `sys.path` even if you accidentally run with system Python  
* 🔄 Auto-enable Django if you request apps or superuser credentials  
* 🔍 Verify that each third-party module actually imports before injecting it  
* 🛠️ Generate helper scripts (`start.sh`, `start.bat`) to activate the venv and run `manage.py runserver`

---

## 🧠 Features

1. **Friendly Web UI** – fill in your project name, check the packages you want, list the apps to create, pick a timezone, and optionally supply superuser credentials.  
2. **Live Streaming Console** – watch real-time updates as folders, virtualenvs, pip installs, Django scaffolding, migrations, and superuser creation happen.  
3. **Timezone Validation** – only accepts valid `zoneinfo` names; falls back to UTC if you enter something invalid.  
4. **Venv Launcher** – prepends a snippet to `manage.py` so it re-executes itself under the venv’s Python interpreter.  
5. **Site-Packages Hack** – prepends a snippet to `settings.py` that ensures your venv’s site-packages directory is on `sys.path`, even under system Python.  
6. **Module Import Checks** – before injecting into `INSTALLED_APPS`, each package is tested with a quick `import`, and only valid ones are added.  
7. **Automatic Migrations** – after scaffolding, runs `manage.py migrate` and streams the output so you don’t have to.  
8. **Superuser Creation** – if you supply a username, email, and password, runs `createsuperuser --noinput` before migrations to seed your admin account.  
9. **Helper Scripts** – two convenience scripts (`start.sh` for Linux/macOS, `start.bat` for Windows) to activate the venv and launch `runserver`.

---

## ⚙️ Requirements

Make sure you have:

* Python **3.8+** (3.12 recommended)  
* `git` and `pip`  

---

## 💾 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/h3xol/django-template-generator.git
   cd django-template-generator
````

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## 🗂️ Project Structure

```
project-root/
├── app.py
├── requirements.txt
├── generated_projects/       # Django projects will be created here
└── templates/
    └── index2.html           # The web UI template
```

---

## ▶️ Usage

1. Start the Flask server:

   ```bash
   python app.py
   ```
2. Open your browser to:

   ```
   http://localhost:5000
   ```
3. Fill out the form (project name, packages, apps, timezone, optional superuser) and hit **Creează proiect**.
4. Watch the live log; when it finishes, you’ll find your new Django project in `generated_projects/<your-project-name>/` with:

   * A fully scaffolded Django project
   * Any apps you requested
   * A virtualenv with all selected packages installed
   * Helper scripts `start.sh` / `start.bat`
   * Database migrations applied
   * (Optional) Superuser account created

---

## ✍️ Author

**Made by [h.s](https://github.com/h3xol)**

```




# 🚀  [RO] Django Template Generator

Un mic generator de proiecte **Django**, construit cu **Flask**, care îți permite să:

* ✅ Creezi un proiect Django nou  
* 📦 Selectezi pachete Python adiționale (`pip`) pentru instalare  
* 🧩 Specifici aplicații Django (`startapp`)  
* 🌍 Definești fusul orar în `settings.py` (validat cu `zoneinfo`)  
* 🔄 Primești un **log în timp real (SSE)** despre stadiul creării proiectului  
* ⚙️ Automat aplici **migrări** (`manage.py migrate`)  
* 🚀 Creezi **superuser** opțional (`createsuperuser --noinput`)  
* 🛡️ „Hacker” `manage.py` pentru a porni mereu sub Python-ul din venv  
* 📌 Injectezi automat `venv`-ul în `sys.path` (site-packages hack)  
* 🔄 Activezi Django automat dacă adaugi apps sau superuser  
* 🔍 Verifici importabilitatea modulelor înainte să le injectezi  
* 🛠️ Primești două scripturi helper (`start.sh`, `start.bat`) pentru a porni serverul  

---

## 🧠 Funcționalități

1. **Interfață web prietenoasă** – completezi nume proiect, bifezi pachete, introduci aplicațiile dorite, alegi fusul orar, opțional superuser.  
2. **Streaming live din consolă** – vezi în timp real pașii de creare (folder, venv, pip install, django-admin, etc).  
3. **Validare timezone** – orice valoare din lista `zoneinfo.available_timezones()`, fallback la UTC.  
4. **Launcher venv** – `manage.py` “se re-execă” automat sub venv/python atunci când îl lansezi.  
5. **Site-packages hack** – dacă rulezi `manage.py` cu sistem Python, tot ți se adaugă venv-ul în `sys.path`.  
6. **Verificare module** – nu injectăm `rest_framework`, `allauth` etc. dacă nu importă.  
7. **Aplicare automată migrări** – după scaffold, rulăm `manage.py migrate` și afișăm progresul în SSE.  
8. **Creare superuser** – înainte de migrări, rulează `createsuperuser --noinput` cu credențiale din formular.  
9. **Scripturi helper** – `start.sh` și `start.bat` configurează automat activarea venv și rularea serverului.  

---

## ⚙️ Precondiții

Asigură-te că ai:

* Python **3.8+** (preferabil 3.12+)  
* `git` și `pip`  

---

## 💾 Instalare

Clonează repo-ul:

```bash
git clone https://github.com/h3xol/django-template-generator.git
cd django-template-generator
````

Instalează dependențele:

```bash
pip install -r requirements.txt
```

---

## 🗂️ Structura proiectului

```
project-root/
├── app.py
├── requirements.txt
├── generated_projects/       # Aici se vor crea proiectele Django
└── templates/
    └── index2.html           # Interfața web
```

---

## ▶️ Utilizare

1. Pornește serverul Flask:

   ```bash
   python app.py
   ```

2. Deschide în browser:

   ```
   http://localhost:5000
   ```

3. Completează formularul (inclusiv superuser dacă vrei) și generează proiectul Django!

4. La final vei avea în `generated_projects/<nume>/`:

   * un proiect Django complet
   * aplicațiile specificate
   * `venv` cu toate pachetele instalate
   * scripturile `start.sh` / `start.bat`
   * baza de date migrată și, dacă ai cerut, un superuser creat

---

## ✍️ Author

**Made by [h.s](https://github.com/h3xol)**

```

