
# 🚀 Django Template Generator

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
```
