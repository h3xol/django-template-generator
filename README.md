# Django Template Generator 

Un mic generator de proiecte Django, construit cu Flask, care îți permite să:

- Creezi un proiect Django nou  
- Selectezi pachete Python adiționale (pip) pentru instalare  
- Specifici aplicații Django (`startapp`) pe care vrei să le generezi  
- Definești fusul orar în `settings.py`  
- Primești un log în timp real (SSE) despre stadiul creării proiectului  
- Primești la final două scripturi helper (`start.sh`, `start.bat`) pentru a porni serverul  

---

## Funcționalități

1. **Interfață web**: completezi nume proiect, bifezi pachete, introduci aplicațiile dorite, alegi fusul orar.  
2. **Streaming de console**: vezi live pașii de creare (folder, venv, pip install, django-admin, injectare setări, crearea app-urilor).  
3. **Injectare automată**: pachetele care corespund unor Django apps și aplicațiile tale apar în `INSTALLED_APPS`.  
4. **Helper scripts**: `start.sh` și `start.bat` configurate automat pentru a porni proiectul în mediul virtual.

---

## Precondiții

- Python 3.8+  
- `git`, `pip`  

---

## Instalare

1. Clonează acest repo:
   ```bash
   git clone https://github.com/utilizator/django-flask-scaffolder.git
   cd django-flask-scaffolder

2. Instalează dependențele:

pip install -r requirements.txt

### Structura proiectului

project-root/

├── app.py

├── requirements.txt

├── generated_projects/       # Aici se vor crea proiectele tale Django

└── templates/
    └── index2.html           # Interfața web

### Utilizare

1. Pornește serverul Flask:
 - python app.py

2. Deschide în browser:

 - http://localhost:5000

3. Completează formularul


### Made by h.s

