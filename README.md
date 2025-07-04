

---

# 🚀 Django Template Generator

Un mic generator de proiecte **Django**, construit cu **Flask**, care îți permite să:

* ✅ Creezi un proiect Django nou
* 📦 Selectezi pachete Python adiționale (`pip`) pentru instalare
* 🧩 Specifici aplicații Django (`startapp`)
* 🌍 Definești fusul orar în `settings.py`
* 🔄 Primești un **log în timp real (SSE)** despre stadiul creării proiectului
* 🛠️ Primești două scripturi helper (`start.sh`, `start.bat`) pentru a porni serverul

---

## 🧠 Funcționalități

1. **Interfață web prietenoasă** – completezi nume proiect, bifezi pachete, introduci aplicațiile dorite, alegi fusul orar.
2. **Streaming live din consolă** – vezi în timp real pașii de creare (folder, venv, pip install, django-admin, etc).
3. **Injectare automată** – pachetele și aplicațiile apar în `INSTALLED_APPS`.
4. **Scripturi helper generate** – `start.sh` și `start.bat` sunt configurate automat pentru pornirea proiectului în mediul virtual.

---

## ⚙️ Precondiții

Asigură-te că ai instalat:

* Python **3.8+**
* `git` și `pip`

---

## 💾 Instalare

Clonează repo-ul:

```bash
git clone https://github.com/h3xol/django-template-generator.git
```

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

3. Completează formularul și generează proiectul Django!

---

## ✍️ Author

**Made by [h.s](https://github.com/h3xol)**

---

