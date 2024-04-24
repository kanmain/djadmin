'''
DjAdmin v1.0.20240424 - bukanmainapp@gmail.com
'''

from decouple import config, Csv

from .base import *

SECRET_KEY = config('SECRET_KEY', cast=str)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

THIRD_PARTY_APPS = config('THIRD_PARTY_APPS', cast=Csv())

CUSTOM_APPS = config('CUSTOM_APPS', cast=Csv())

INSTALLED_APPS = INSTALLED_APPS + THIRD_PARTY_APPS + CUSTOM_APPS
