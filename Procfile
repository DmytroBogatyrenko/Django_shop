web: python manage.py migrate --settings=shop_project.settings_production && gunicorn shop_project.wsgi:application --bind 0.0.0.0:$PORT
