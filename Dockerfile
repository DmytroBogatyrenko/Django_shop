# Беремо офіційний Python 3.13 на мінімальному Linux (slim = без зайвих пакетів)
FROM python:3.13-slim

# Встановлюємо робочу папку всередині контейнера
WORKDIR /app

# Копіюємо спочатку тільки requirements.txt і встановлюємо залежності.
# Хитрість: якщо код змінився але requirements.txt ні — Docker не буде
# перевстановлювати пакети, просто візьме з кешу. Значно швидше.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Тепер копіюємо весь код проєкту
COPY . .

# Збираємо статичні файли в одну папку (для WhiteNoise)
RUN python manage.py collectstatic --noinput --settings=shop_project.settings_production

# Порт на якому слухає наш застосунок
EXPOSE 8000

# Gunicorn — продакшн-сервер.
# manage.py runserver призначений тільки для розробки — повільний, небезпечний.
# Gunicorn запускає кілька "воркерів" що обробляють запити паралельно.
CMD ["gunicorn", "shop_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
