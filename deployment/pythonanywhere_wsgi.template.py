"""Copy this into the WSGI file linked from PythonAnywhere's Web tab.

Replace the username, project path, domain, and secret before saving.
Do not put this template or the real secret into a public repository.
"""
import os
import sys

username = "YOUR_PYTHONANYWHERE_USERNAME"
project_home = os.path.expanduser(f"~/autocraft")
domain = f"{username}.pythonanywhere.com"
secret_key = "REPLACE_WITH_A_NEW_DJANGO_SECRET_KEY"

if secret_key.startswith("REPLACE_"):
    raise RuntimeError("Set a private DJANGO_SECRET_KEY in the PythonAnywhere WSGI file.")

if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ["DJANGO_SETTINGS_MODULE"] = "autocraft.settings"
os.environ["DJANGO_SECRET_KEY"] = secret_key
os.environ["DJANGO_DEBUG"] = "0"
os.environ["DJANGO_ALLOWED_HOSTS"] = domain
os.environ["DJANGO_CSRF_TRUSTED_ORIGINS"] = f"https://{domain}"

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
