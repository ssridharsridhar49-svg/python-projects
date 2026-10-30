# AutoCraft

AutoCraft is a Django car and bike customization site. Vehicle catalogs are separate, and each saved build is connected to the signed-in user and vehicle in SQLite.

## Run locally

Use Python 3.10 or newer. From this folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/>. For a new installation, create an administrator with:

```powershell
python manage.py createsuperuser
```

Then open <http://127.0.0.1:8000/admin/> to manage users, vehicles, saved designs, and contact messages. New user passwords are stored using Django's password hashing; they are never saved as plain text.

## Features

- Separate car and bike catalogs and modification URLs.
- Live build preview for paint, wheels, spoiler or tail, graphics, exhaust, and category-specific accessories.
- Saved designs stored against the user's account. A guest's selections are retained through login before the design is saved.
- Django Admin screens for registered users, vehicles, designs, and contact submissions.
- SQLite database and local media storage. Catalog images may use an uploaded local file or a hosted image URL.

Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, and `DJANGO_ALLOWED_HOSTS` in the environment before deploying outside local development.

See [DEPLOY_RENDER.md](DEPLOY_RENDER.md) for the Render Blueprint setup and [DEPLOY_PYTHONANYWHERE.md](DEPLOY_PYTHONANYWHERE.md) for PythonAnywhere.
