from decouple import config
from .public import *

DEBUG = config('DEBUG', cast=bool, default=False)

DATABASES = {
    'default': {
      'ENGINE': config('DATABASES_ENGINE'),
      'HOST': config('DATABASES_HOST'),
      'NAME': config('DATABASES_NAME'),
      'USER': config('DATABASES_USER'),
      'PORT': config('DATABASES_PORT', cast=int),
      'PASSWORD': config('DATABASES_PASSWORD'),
  }
}