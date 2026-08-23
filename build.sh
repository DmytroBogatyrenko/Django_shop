#!/usr/bin/env bash

pip install -r requirements.txt

python manage.py collectstatic --noinput

# Застосовуємо ВСІ міграції включно з новими (reviews, allauth, sites)
python manage.py migrate --run-syncdb

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

# Виправляємо Site — замінюємо example.com на реальний домен
python manage.py shell -c "
from django.contrib.sites.models import Site
site, created = Site.objects.get_or_create(id=1)
site.domain = 'djangoshop-sg08.onrender.com'
site.name = 'Citadel Shop'
site.save()
print('Site налаштовано:', site.domain)
"

# Створюємо суперюзера якщо його ще немає
python manage.py createsuperuser --noinput 2>/dev/null || echo "Суперюзер вже є"