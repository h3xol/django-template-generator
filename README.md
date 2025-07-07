![image](https://github.com/user-attachments/assets/997e3766-b74c-48b5-a001-287cdb532d44)

# 🚀 [EN] Django Template Generator

A lightweight **Django** project generator built with **Flask** that enables you to:

- ✅ Create a brand-new Django project  
- 📦 Choose extra Python packages to install (`pip install`)  
- 🧩 Scaffold Django apps (`startapp`)  
- 🌍 Set and validate `TIME_ZONE` in `settings.py` (using `zoneinfo`)  
- 🔄 Stream a **live console log (SSE)** of every generation step  
- ⚙️ Automatically apply database **migrations** (`manage.py migrate`)  
- 🚀 Optionally create a **superuser** (`createsuperuser --noinput`)  
- 🛡️ Inject a small launcher into `manage.py` so it always runs under the virtualenv’s Python  
- 📌 Prepend your virtualenv’s `site-packages` to `sys.path` even if you launch with system Python  
- 🔍 Verify that each selected package actually imports before adding it to `INSTALLED_APPS`  
- 🛠️ Generate helper scripts (`start.sh` and `start.bat`) that activate the venv and start the development server  

---

## 🧠 Key Features

1. **Friendly Web UI**  
   Fill in your project name, check the packages you want, list apps to create, choose a timezone, and supply optional superuser credentials.

2. **Live Streaming Console**  
   Watch real-time updates as folders are created, a virtualenv is set up, packages install, Django scaffolding runs, migrations apply, and a superuser is created.

3. **Timezone Validation**  
   Accepts only valid `zoneinfo.available_timezones()` values; falls back to `UTC` if you enter something unsupported.

4. **Virtualenv Launcher**  
   Prepends a snippet to `manage.py` so it automatically re-executes itself under the virtualenv’s Python interpreter.

5. **Site-Packages Hack**  
   Adds your project’s `venv/lib/pythonX.Y/site-packages` (or `Scripts/Lib/site-packages` on Windows) to `sys.path`, ensuring missing apps don’t cause import errors.

6. **Module Import Checks**  
   Runs a quick `import <module>` for each selected package and injects only those that succeed.

7. **Automatic Migrations**  
   Runs `manage.py migrate` and streams the output so you don’t have to invoke it manually.

8. **Superuser Creation**  
   If you provide a username, email, and password, runs `createsuperuser --noinput` before migrations to seed your admin account.

9. **Helper Scripts**  
   Generates `start.sh` (for Linux/macOS) and `start.bat` (for Windows) that activate the venv and launch `python manage.py runserver`.

---

## ⚙️ Requirements

- Python **3.8+** (3.12 recommended)  
- `git`  
- `pip`

---

## 💾 Installation

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


---

## 🗂️ Project Structure

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
├── generated_projects/    # Newly generated Django projects go here
└── templates/
    └── index.html        # The web UI template
├── generated_projects/       # Aici se vor crea proiectele Django
└── templates/

```

---

## ▶️ Usage

1. Start the Flask server:

   ```bash
   python app.py
   ```

2. Open your browser at:

   ```
   http://localhost:5000
   ```

3. Fill out the form (project name, packages, apps, timezone, optional superuser) and click **“Creează proiect”**.

4. Watch the live console log; when finished, your new Django project will be in:

   ```
   generated_projects/<your-project-name>/
   ```

   You’ll find:

   * A fully scaffolded Django project
   * Any apps you requested
   * A virtualenv with all selected packages installed
   * Helper scripts (`start.sh` / `start.bat`)
   * Database migrations applied
   * (Optional) Superuser account created

---

# 🚀 [RO] Django Template Generator

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
    └── index.html           # Interfața web
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
