from decouple import config
from .public import *

DEBUG = config('DEBUG', cast=bool, default=True)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
