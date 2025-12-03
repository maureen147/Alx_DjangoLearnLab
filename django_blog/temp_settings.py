# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'USER': '',      # SQLite doesn't use user, but we'll add it
        'PASSWORD': '',  # SQLite doesn't use password
        'HOST': '',      # SQLite doesn't use host
        'PORT': '',      # SQLite doesn't use port
    }
}
