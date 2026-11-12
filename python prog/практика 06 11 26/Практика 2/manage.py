# Практика 2. Откройте терминал в этой папке и выполните:
# python -m pip install -r requirements.txt
# python manage.py runserver
# После запуска откройте http://127.0.0.1:8000/ в браузере.
# Для остановки сервера нажмите Ctrl+C в терминале.

import os
import sys

from django.core.management import execute_from_command_line


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    execute_from_command_line(sys.argv)
