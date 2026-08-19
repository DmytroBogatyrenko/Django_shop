from .settings import *
import os

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':     os.environ.get('PGDATABASE'),
        'USER':     os.environ.get('PGUSER'),
        'PASSWORD': os.environ.get('PGPASSWORD'),
        'HOST':     os.environ.get('PGHOST'),
        'PORT':     os.environ.get('PGPORT', '5432'),
    }
}


MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True    
SECURE_CONTENT_TYPE_NOSNIFF = True 