from pathlib import Path

DEBUG = True
ALLOWED_HOSTS = ['*']

HOME_DIR = Path.home()
STATIC_ROOT = HOME_DIR.joinpath("var/jerseystuff/static/")