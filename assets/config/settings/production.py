from decouple import config
from .public import *

DEBUG = config('DEBUG', cast=bool, default=False)
