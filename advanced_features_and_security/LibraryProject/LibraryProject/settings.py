"""
Django settings for LibraryProject project.

SECURITY CONFIGURATION:
This configuration includes comprehensive security settings for HTTPS enforcement,
secure cookies, and security headers to protect against common web vulnerabilities.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$+52(ulh)0bw20&jqazs&y33n(z0_&d=q1299p)%i_4r0$)#_#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow localhost for development and example domains for production
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'example.com', 'www.example.com']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookshelf',
    'relationship_app',
]

# Custom user model
AUTH_USER_MODEL = 'bookshelf.CustomUser'

# =============================================================================
# HTTPS AND SECURITY CONFIGURATION
# =============================================================================

# SECURITY: HTTPS Configuration
# Set to True to redirect all HTTP requests to HTTPS
SECURE_SSL_REDIRECT = True

# SECURITY: HTTP Strict Transport Security (HSTS)
# Instruct browsers to only access the site via HTTPS for one year
SECURE_HSTS_SECONDS = 31536000  # 1 year in seconds

# SECURITY: Include all subdomains in HSTS policy
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# SECURITY: Allow HSTS preloading (submit to browser preload lists)
SECURE_HSTS_PRELOAD = True

# SECURITY: Secure Cookies - Only send over HTTPS
SESSION_COOKIE_SECURE = True      # Session cookies only over HTTPS
CSRF_COOKIE_SECURE = True         # CSRF cookies only over HTTPS

# SECURITY: Additional Security Headers
SECURE_BROWSER_XSS_FILTER = True  # Enable browser XSS filtering
SECURE_CONTENT_TYPE_NOSNIFF = True # Prevent MIME type sniffing
X_FRAME_OPTIONS = 'DENY'          # Prevent clickjacking by denying framing

# SECURITY: Referrer Policy
SECURE_REFERRER_POLICY = 'same-origin'  # Only send referrer for same-origin requests

# SECURITY: Content Security Policy (Basic - for more advanced CSP, use django-csp)
# Note: CSP headers are also set in templates via meta tags

# Middleware configuration with security middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]

ROOT_URLCONF = 'LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LibraryProject.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging configuration for security monitoring
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'security.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'bookshelf': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# =============================================================================
# DEVELOPMENT OVERRIDES
# Comment out the following section in production
# =============================================================================

# For development only - disable HTTPS redirect and secure cookies
if DEBUG:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0  # Disable HSTS in development
    print("⚠️  DEVELOPMENT MODE: HTTPS security settings disabled")
EOFcat > LibraryProject/LibraryProject/settings.py << 'EOF'
"""
Django settings for LibraryProject project.

SECURITY CONFIGURATION:
This configuration includes comprehensive security settings for HTTPS enforcement,
secure cookies, and security headers to protect against common web vulnerabilities.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$+52(ulh)0bw20&jqazs&y33n(z0_&d=q1299p)%i_4r0$)#_#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow localhost for development and example domains for production
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'example.com', 'www.example.com']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookshelf',
    'relationship_app',
]

# Custom user model
AUTH_USER_MODEL = 'bookshelf.CustomUser'

# =============================================================================
# HTTPS AND SECURITY CONFIGURATION
# =============================================================================

# SECURITY: HTTPS Configuration
# Set to True to redirect all HTTP requests to HTTPS
SECURE_SSL_REDIRECT = True

# SECURITY: HTTP Strict Transport Security (HSTS)
# Instruct browsers to only access the site via HTTPS for one year
SECURE_HSTS_SECONDS = 31536000  # 1 year in seconds

# SECURITY: Include all subdomains in HSTS policy
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# SECURITY: Allow HSTS preloading (submit to browser preload lists)
SECURE_HSTS_PRELOAD = True

# SECURITY: Secure Cookies - Only send over HTTPS
SESSION_COOKIE_SECURE = True      # Session cookies only over HTTPS
CSRF_COOKIE_SECURE = True         # CSRF cookies only over HTTPS

# SECURITY: Additional Security Headers
SECURE_BROWSER_XSS_FILTER = True  # Enable browser XSS filtering
SECURE_CONTENT_TYPE_NOSNIFF = True # Prevent MIME type sniffing
X_FRAME_OPTIONS = 'DENY'          # Prevent clickjacking by denying framing

# SECURITY: Referrer Policy
SECURE_REFERRER_POLICY = 'same-origin'  # Only send referrer for same-origin requests

# SECURITY: Content Security Policy (Basic - for more advanced CSP, use django-csp)
# Note: CSP headers are also set in templates via meta tags

# Middleware configuration with security middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]

ROOT_URLCONF = 'LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LibraryProject.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging configuration for security monitoring
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'security.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'bookshelf': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# =============================================================================
# DEVELOPMENT OVERRIDES
# Comment out the following section in production
# =============================================================================

# For development only - disable HTTPS redirect and secure cookies
if DEBUG:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0  # Disable HSTS in development
    print("⚠️  DEVELOPMENT MODE: HTTPS security settings disabled")
