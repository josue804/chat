"""
WSGI config for hpc project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
# from whitenoise.django import DjangoWhiteNoise
from django.conf import settings
from whitenoise import WhiteNoise

if settings.DEBUG:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings.base")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings.production")

application = get_wsgi_application()
application = WhiteNoise(application, root=os.path.join(settings.PROJECT_DIR, 'staticfiles'))
application.add_files(os.path.join('media', 'CACHE', 'images', 'avatar'), prefix=settings.PROJECT_DIR)
