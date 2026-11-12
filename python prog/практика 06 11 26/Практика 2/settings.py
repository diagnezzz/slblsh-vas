from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = "local-dog-api-practice-only"
DEBUG = True  # Настройки для учебного запуска на своём компьютере.
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

ROOT_URLCONF = "urls"
INSTALLED_APPS = []
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

# Говорим Django, где находится HTML-шаблон страницы.
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": False,
}]

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_TZ = True
