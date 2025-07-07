
# 🚀 Django Template Generator

Un generator simplu de proiecte **Django**, construit cu **Flask**, care îți permite:

- ✅ Să creezi un proiect Django nou  
- 📦 Să selectezi pachete Python adiționale (`pip install`)  
- 🧩 Să specifici aplicații Django de creat (`startapp`)  
- 🌍 Să setezi fusul orar în `settings.py` (validat cu `zoneinfo`)  
- 🔄 Să primești un **log în timp real (SSE)** al procesului de generare  
- ⚙️ Să rulezi automat **migrările** (`manage.py migrate`)  
- 🚀 Să creezi opțional un **superuser** (`createsuperuser --noinput`)  
- 🛡️ Să „hack-uiești” `manage.py` pentru a se lansa întotdeauna cu Python-ul din venv  
- 📌 Să injectezi automat `site-packages`-ul din venv în `sys.path`  
- 🔍 Să verifici că fiecare modul importă înainte de a fi adăugat în `INSTALLED_APPS`  
- 🛠️ Să primești scripturi helper (`start.sh`, `start.bat`) care activează venv-ul și pornesc serverul  

---

## 📖 English

### Features

1. **Friendly Web UI**  
   Completezi numele proiectului, bifezi pachete, listezi aplicațiile, alegi fusul orar și (opțional) superuser-ul.  
2. **Live Streaming Console**  
   Urmărești în timp real pașii: creare folder, venv, pip install, django-admin, apps, migrări și superuser.  
3. **Timezone Validation**  
   Acceptă doar fusuri orare din `zoneinfo.available_timezones()`, fallback la `UTC`.  
4. **Venv Launcher**  
   Prependă un snippet în `manage.py` pentru a-l re-execu­ta sub venv-ul Python.  
5. **Site-Packages Hack**  
   Injectează venv-ul în `sys.path` chiar dacă rulezi cu sistem Python.  
6. **Module Import Checks**  
   Verifică cu `import modul` înainte de a-l include în `INSTALLED_APPS`.  
7. **Automatic Migrations**  
   Rulează `manage.py migrate` și streamează ieșirea în SSE.  
8. **Superuser Creation**  
   Dacă furnizezi nume, email și parolă, rulează `createsuperuser --noinput` înainte de migrări.  
9. **Helper Scripts**  
   `start.sh` (Linux/macOS) și `start.bat` (Windows) pentru activarea venv și `runserver`.

### Requirements

- Python **3.8+** (3.12 recomandat)  
- `git`, `pip`

### Installation

```bash
git clone https://github.com/h3xol/django-template-generator.git
cd django-template-generator
pip install -r requirements.txt
````

### Project Structure

```
project-root/
├── app.py
├── requirements.txt
├── generated_projects/    # Aici vor apărea proiectele Django create
└── templates/
    └── index2.html        # Interfața web
```

### Usage

1. Pornește serverul Flask:

   ```bash
   python app.py
   ```

2. Deschide browser-ul la:

   ```
   http://localhost:5000
   ```

3. Completează formularul și apasă **Creează proiect**.

4. Urmărește log-ul în timp real; la final, găsești proiectul Django în:

   ```
   generated_projects/<project-name>/
   ```

   – Conține proiectul Django
   – Aplicațiile tale
   – `venv` cu pachetele instalate
   – Scripturile `start.sh` / `start.bat`
   – Baza de date migrată
   – (Opțional) Superuser creat

---

## 📖 Română

### Funcționalități

1. **Interfață web prietenoasă**
2. **Streaming live din consolă**
3. **Validare fus orar**
4. **Launcher venv în `manage.py`**
5. **Site-packages hack**
6. **Verificare import module**
7. **Aplicare migrări automatic**
8. **Creare superuser opțional**
9. **Scripturi helper**

### Precondiții

* Python **3.8+**, `git` și `pip`

### Instalare

```bash
git clone https://github.com/h3xol/django-template-generator.git
cd django-template-generator
pip install -r requirements.txt
```

### Structura proiectului

```
project-root/
├── app.py
├── requirements.txt
├── generated_projects/
└── templates/
    └── index2.html
```

### Utilizare

1. `python app.py`
2. Accesează `http://localhost:5000`
3. Completează formularul și creează proiectul
4. Găsești rezultatul în `generated_projects/<nume>/`

---

## ✍️ Author

**Made by [h.s](https://github.com/h3xol)**


