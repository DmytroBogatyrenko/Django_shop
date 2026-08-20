#!/usr/bin/env bash
# Вихід при будь-якій помилці скрипта
set -o errexit

# Встановлення залежностей
pip install -r requirements.txt

# Збір статичних файлів
python manage.py collectstatic --no-input

# Запуск міграцій бази даних
python manage.py migrate
