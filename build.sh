#!/usr/bin/env bash

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate

# Заповнюємо базу даних тільки якщо товарів ще немає
# Це важливо — щоб при кожному наступному деплої не дублювались дані
python manage.py shell -c "
from shop.models import Product
if Product.objects.count() == 0:
    from django.core.management import call_command
    call_command('populate_db')
    print('База заповнена товарами')
else:
    print('Товари вже є, пропускаємо')
"

# Створюємо суперюзера якщо його ще немає
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@citadel.ua',
        password='Citadel2026!'
    )
    print('Суперюзер створений: admin / Citadel2026!')
else:
    print('Суперюзер вже є')
"