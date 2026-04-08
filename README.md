# AI Tor Gorag Platformasy (Django)

Bu taslama tor traffiginde şübheli hereketleri **AI** kömegi bilen tapmak üçin döredilen köp sahypaly web-platformadyr.

## Funksiýalar

- Turkmençe interfeýs: ähli düwmeler, menýular, habarlar.
- Hasaba almak / giriş (sessiýa authentication), admin rol dolandyryşy.
- Dolandyryş paneli: grafikler (Chart.js), howp derejeleri, real-time duýduryşlar (WebSocket).
- Tor traffiginiň analizi: CSV log ýüklemek, awtomat anomaliýa barlagy.
- AI model dolandyryşy: Random Forest, Neural Network, Logistic Regression tälimi we metrikalar.
- Duýduryşlar: hüjüm klassifikasiýasy (DDoS, phishing, malware), süzgüç.
- Ulanyjy dolandyryşy: admin üçin CRUD (sanaw + redaktirleme).
- Hasabatlar: hüjüm taryhy, CSV eksport.
- Sazlamalar: API açarlary / threshold / email (demo görnüşde).
- REST API: `/api/stats/`, `/api/detect/`, `/api/token/`.

## Tehnologiýalar

- Backend: Django + Channels
- Frontend: HTML/CSS/JavaScript
- DB: SQLite (default), PostgreSQL (env arkaly)
- ML: scikit-learn

## Gurnama

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```


## Windows (OSGeo4W) ýalňyşlygyny düzetmek

Eger şeýle ýalňyşlyk alsaňyz: `ModuleNotFoundError: No module named encodings` ýa-da `C:\OSGeo4W\bin\python3.exe`, onda OSGeo-nyň Python-y bilen işe girýärsiňiz.

### Çalt usul (awtomat skript)

```powershell
cd <taslama-papkasy>
PowerShell -ExecutionPolicy Bypass -File .\scripts\bootstrap_windows.ps1
```

### El bilen usul

`docs/WINDOWS_TROUBLESHOOTING.md` faýlyndaky ädimleri ýerine ýetiriň.

## PostgreSQL ulanmak

```bash
export DB_ENGINE=django.db.backends.postgresql
export DB_NAME=networksecure
export DB_USER=postgres
export DB_PASSWORD=postgres
export DB_HOST=127.0.0.1
export DB_PORT=5432
python manage.py migrate
```

## Ulanyjy maglumatlary (demo)

- Admin: `admin`
- Açar söz: `admin12345`

## API ulanylyşy

### Token almak
```bash
curl -X POST http://127.0.0.1:8000/api/token/ -H 'Content-Type: application/json' -d '{"username":"admin","password":"admin12345"}'
```

### Anomaliýa barlagy
```bash
curl -X POST http://127.0.0.1:8000/api/detect/ -H 'Content-Type: application/json' -d '{"bytes_transferred":71000}'
```

### Statistika
```bash
curl http://127.0.0.1:8000/api/stats/
```

## Taslama gurluşy

- `config/` — Django sazlamalary (WSGI/ASGI, URLs, DB, Channels)
- `platformapp/models.py` — trafik, howp, duýduryş, AI model ýazgylary
- `platformapp/views.py` — ähli sahypalar we API endpointler
- `platformapp/services/ml_service.py` — ML tälim logikasy
- `platformapp/consumers.py` — WebSocket duýduryş consumer
- `platformapp/templates/platformapp/` — ähli HTML sahypalar
- `platformapp/static/platformapp/` — CSS/JS
- `data/sample_traffic.csv` — test log nusgasy

## Howpsuzlyk bellikler

- Django ORM SQL injection töwekgelçiligini azaltýar.
- CSRF goragy ähli formalar üçin açyk.
- Ulanyjy hereketleri `UserActionLog` arkaly ýazga alnyp bilner.
- Session auth + JWT token endpoint bar.

