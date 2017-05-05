import os
from .base import *

DEBUG = False
SECRET_KEY = os.environ.get('HPC_SECRET_KEY')
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
