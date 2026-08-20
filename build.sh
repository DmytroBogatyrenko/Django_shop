#!/usr/bin/env bash

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate

# Заповнюємо базу тільки якщо товарів ще немає
python manage.py shell -c "
from shop.models import Product
if Product.objects.count() == 0:
    from django.core.management import call_command
    call_command('populate_db')
    print('База заповнена')
else:
    print('Товари вже є')
"

# Створюємо суперюзера з змінних середовища — пароль не в коді
# DJANGO_SUPERUSER_* — стандартні змінні які Django розуміє сам
python manage.py createsuperuser --noinput 2>/dev/null || echo "Суперюзер вже є"