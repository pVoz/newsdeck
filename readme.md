# NewsDeck (Django + Celery)

Projekt na sťahovanie RSS článkov a tvorbu **digestov**.
- **Django**: modely `NewsSource`, `Article`, `Digest` + admin
- **Celery**: úloha `fetch_rss_feeds` + periodické spúšťanie (beat)
- **Redis**: broker + výsledky
- **Python 3.12**, Dockerfile pripravený, **docker-compose** pridaný

---

## Rýchly štart (lokálne, dev)

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Spusti **Celery** (dve okná):
```bash
# worker
celery -A newsdeck worker -l info

# beat (plánovač)
celery -A newsdeck beat -l info
```

---

## Env premenné (dev)
Vytvor `.env` alebo nastav v shelli:
```
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
DJANGO_SETTINGS_MODULE=newsdeck.settings
```

---

## Docker (jednoducho)

### Build & run (single container)
```bash
docker build -t newsdeck .
docker run --env-file .env -p 8000:8000 newsdeck
```
> Pozn.: Tento mód nespúšťa Redis ani Celery – vhodné len na rýchle overenie webu.

---

## Docker Compose (web + redis + celery worker + beat)

1) Uisti sa, že máš `.env` v koreňovom priečinku repozitára:
```
# .env (compose používa hostname 'redis')
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
DJANGO_SETTINGS_MODULE=newsdeck.settings
```

2) Spusť kontajnery:
```bash
docker compose up --build
```

3) Vykonaj migrácie a vytvor admina:
```bash
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py createsuperuser
```

4) Aplikácia beží na: http://localhost:8000  
   Admin: http://localhost:8000/admin

> Štandardný dev stack:
> - `web` – Django
> - `redis` – broker + backend
> - `celery-worker` – tasky
> - `celery-beat` – plánovač taskov

---

## Súbory, ktoré ma zaujímajú
- `feeds/models.py` – modely `NewsSource`, `Article`, `Digest`, `DigestArticle`
- `feeds/admin.py` – admin
- `feeds/tasks.py` – Celery úlohy (`fetch_rss_feeds`)
- `newsdeck/celery.py` – celery inicializácia
- `newsdeck/settings.py` – celery nastavenia + beat schedule
- `docker-compose.yml` – spustenie webu + redis + celery (dev)

---

## Poznámky
- **Dev režim**: `DEBUG=True`, SQLite (`db.sqlite3`)
- **Prod**: nastav `SECRET_KEY` a `DEBUG=False` v prostredí, zváž PostgreSQL a `gunicorn/uvicorn`
- `Article.link` je unikátny (ochrana proti duplicitám)
- `CELERY_BEAT_SCHEDULE` = 15 minút 
