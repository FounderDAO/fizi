from .base import *

DEBUG = True
CORS_ALLOW_ALL_ORIGINS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable storages for tests
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
