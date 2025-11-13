"""
Production-specific settings for LibraryProject.
"""
from .settings import *

# Override for production
DEBUG = False

# Security settings for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year

# Generate a proper secret key for production
SECRET_KEY = 'your-production-secret-key-here-make-it-long-and-random'

# Remove development overrides
print("í´’ PRODUCTION MODE: All security settings enabled")
