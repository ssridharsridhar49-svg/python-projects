# PythonAnywhere deployment

This repository is prepared for PythonAnywhere. A PythonAnywhere account is required to create the public `USERNAME.pythonanywhere.com` site. The deployment uses SQLite, Django's WSGI application, `collectstatic`, and PythonAnywhere's `/static/` and `/media/` file mappings.

## Upload and install

1. Create a PythonAnywhere account and add a **Manual configuration** web app. Choose an available Python version supported by the account's system image (Python 3.13 is available on current images).
2. Upload `autocraft_corrected_project.zip` using the **Files** tab. In a Bash console, extract it to `~/autocraft`:

   ```bash
   mkdir -p ~/autocraft
   unzip -o ~/autocraft_corrected_project.zip -d ~/autocraft
   cd ~/autocraft
   ```

3. Create the virtual environment with the same Python version selected for the web app, then install requirements. Example for Python 3.13:

   ```bash
   python3.13 -m venv ~/.virtualenvs/autocraft
   source ~/.virtualenvs/autocraft/bin/activate
   python -m pip install -r ~/autocraft/requirements.txt
   python ~/autocraft/manage.py migrate
   python ~/autocraft/manage.py collectstatic --noinput
   ```

   Set the web app's **Virtualenv** field to `/home/YOUR_USERNAME/.virtualenvs/autocraft`.

## WSGI and security

1. Generate a new secret on the PythonAnywhere Bash console (with the virtualenv activated):

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. Open the WSGI file linked from the **Web** tab. Replace its contents with `deployment/pythonanywhere_wsgi.template.py`, then replace the username and secret placeholders. Keep the real secret only in the private WSGI file; do not add it to the ZIP or a public repository.
3. In the **Web** tab, enable **Force HTTPS** after the site has been created. The app sets `DEBUG=False`, restricts `ALLOWED_HOSTS` to the PythonAnywhere domain, uses secure session and CSRF cookies, and recognizes PythonAnywhere's HTTPS proxy header.

The uploaded SQLite database carries the existing project data. New signups, designs, and contact messages will be written to the same database. The existing `media/vehicles/Yamaha_R1_.jpg` image is included.

## Static and uploaded media mappings

After `collectstatic`, add these mappings under **Static files** on the **Web** tab, substituting the account username:

| URL | Directory |
| --- | --- |
| `/static/` | `/home/YOUR_USERNAME/autocraft/staticfiles` |
| `/media/` | `/home/YOUR_USERNAME/autocraft/media` |

Reload the web app. Visit `/static/garage/css/style.css` and `/media/vehicles/Yamaha_R1_.jpg` directly to verify both mappings. Re-run `collectstatic` and reload after publishing future CSS or JavaScript changes.

## Final checks

From the Bash console:

```bash
cd ~/autocraft
source ~/.virtualenvs/autocraft/bin/activate
python manage.py check
python manage.py showmigrations
```

Then reload the web app and open `https://YOUR_USERNAME.pythonanywhere.com/`. Test signup, login, a car build, a bike build, and `/admin/`. If an administrator account is needed, create one with `python manage.py createsuperuser`.
