import os
from .base import *

DEBUG = False
SECRET_KEY = os.environ.get('HPC_SECRET_KEY')
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
