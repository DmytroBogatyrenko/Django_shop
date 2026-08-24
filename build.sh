#!/usr/bin/env bash

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate --run-syncdb

# Окремо мігруємо sites — без цього adмінка падає з 500
python manage.py migrate sites

python manage.py shell -c "
from shop.models import Product
if Product.objects.count() == 0:
    from django.core.management import call_command
    call_command('populate_db')
    print('База заповнена')
else:
    print('Товари вже є')
"

python manage.py shell -c "
from django.contrib.sites.models import Site
site, created = Site.objects.get_or_create(id=1)
site.domain = 'django-shop-backend.onrender.com'
site.name = 'Citadel Shop'
site.save()
print('Site налаштовано:', site.domain)
"

python manage.py createsuperuser --noinput 2>/dev/null || echo "Суперюзер вже є"