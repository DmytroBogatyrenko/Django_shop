"""
Налаштування для продакшну (Render.com).
Імпортуємо все з settings.py і перевизначаємо тільки потрібне.
"""
from .settings import *
import os

# ── Безпека ────────────────────────────────────────────────────────────────────
SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# ── База даних ─────────────────────────────────────────────────────────────────
# Render передає все одним рядком DATABASE_URL.
# dj-database-url розбирає його на окремі поля автоматично.
import dj_database_url

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,  # тримаємо зʼєднання відкритим 10 хвилин
        )
    }

# ── Redis ──────────────────────────────────────────────────────────────────────
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

# ── Статичні файли — WhiteNoise ────────────────────────────────────────────────
# WhiteNoise роздає static файли прямо з Django без окремого nginx
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ── HTTPS ──────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'debug_toolbar']
MIDDLEWARE = [m for m in MIDDLEWARE if 'debug_toolbar' not in m]
SECURE_SSL_REDIRECT = False
# Вимикаємо debug toolbar в продакшні — він може ламати адмінку
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Render використовує proxy — Django має довіряти заголовку X-Forwarded-For
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Кажемо Django що він за proxy — тоді він правильно читає
# реальний IP з заголовка X-Forwarded-For
USE_X_FORWARDED_HOST = True
RATELIMIT_FAIL_OPEN = True  # якщо не вдалось визначити IP — пропускаємо, не блокуємо
