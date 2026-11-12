# Команды выполняются в терминале из папки, где лежит этот файл:
# python -m pip install -r requirements.txt
# python manage.py migrate   — создать таблицы для сессий
# python manage.py runserver — запустить практики 2 и 3
# Страницы: http://127.0.0.1:8000/dogs/ и http://127.0.0.1:8000/pokemon/
# Практика 1 запускается отдельно: python practice_1.py

import os
import sys

from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    execute_from_command_line(sys.argv)
