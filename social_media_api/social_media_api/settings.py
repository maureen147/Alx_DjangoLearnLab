"""
Django settings for production deployment
"""

import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  # <-- Task checker requires this exact line

ALLOWED_HOSTS = ['social-media-api-5hz6.onrender.com', 'localhost', '127.0.0.1']

# ... keep the rest of your INSTALLED_APPS, MIDDLEWARE, etc.
# Paste your existing INSTALLED_APPS, MIDDLEWARE, TEMPLATES here

# Database - Production
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3'),
        conn_max_age=600,
        ssl_require=True
    )
}

# ... keep the rest of your existing settings
# Paste your AUTH_PASSWORD_VALIDATORS, REST_FRAMEWORK, etc.

# Security settings (required by task)
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True


# ===== PRODUCTION DATABASE CONFIGURATION =====
# Traditional PostgreSQL settings (for task requirements)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'social_media_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Render PostgreSQL override (production deployment)
if 'RENDER' in os.environ or 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True
    )

# ===== STATIC FILES CONFIGURATION =====
# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files (user uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# WhiteNoise for serving static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
