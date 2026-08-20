"""
Налаштування для продакшну (Render.com).
Імпортуємо все з settings.py і перевизначаємо тільки потрібне.
"""
import os
from .settings import *
import dj_database_url

# ── 1. БЕЗПЕКА ТА КЛЮЧІ ────────────────────────────────────────────────────────
# Безпечно зчитуємо SECRET_KEY з Environment Variables у Render
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-insecure-key-for-build-only')

# На продакшні DEBUG обов'язково має бути False
DEBUG = False

# Дозволені хости
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '://onrender.com,*.onrender.com').split(',')


# ── 2. СИСТЕМНІ КОРЕКЦІЇ (ВИМКНЕННЯ DEBUG TOOLBAR) ──────────────────────────────
# Видаляємо debug_toolbar з пакунків та middleware, щоб сайт не падав у продакшні
if 'debug_toolbar' in INSTALLED_APPS:
    INSTALLED_APPS.remove('debug_toolbar')

if 'debug_toolbar.middleware.DebugToolbarMiddleware' in MIDDLEWARE:
    MIDDLEWARE.remove('debug_toolbar.middleware.DebugToolbarMiddleware')


# ── 3. БАЗА ДАНИХ (POSTGRESQL) ──────────────────────────────────────────────────
# Render автоматично передає DATABASE_URL. Якщо її немає — залишається SQLite з settings.py
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,  # Тримаємо зʼєднання відкритим 10 хвилин для швидкості
        )
    }


# ── 4. КЕШУВАННЯ ТА REDIS ───────────────────────────────────────────────────────
REDIS_URL = os.environ.get('REDIS_URL')
if REDIS_URL:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'IGNORE_EXCEPTIONS': True,
            },
            'TIMEOUT': 60 * 15,
        }
    }


# ── 5. СТАТИЧНІ ФАЙЛИ ТА WHITENOISE (DJANGO 6.0+) ────────────────────────────────
# WhiteNoise робить так, щоб Django сам віддавав CSS/JS файли без Nginx
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_ROOT = BASE_DIR / 'staticfiles'

# Сучасний формат конфігурації сховища (STORAGES) для Django 6.x
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# ── 6. БЕЗПЕКА HTTPS ТА ВИПРАВЛЕННЯ ПОМИЛКИ 403 (CSRF) ─────────────────────────
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Render працює через проксі — Django має знати, що запит прийшов через HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ВИПРАВЛЕННЯ ПОМИЛКИ 403: Дозволяємо вашому домену Render надсилати POST-форми (реєстрація, кошик)
CSRF_TRUSTED_ORIGINS = [
    'https://://onrender.com',
]
