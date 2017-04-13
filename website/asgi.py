import os
import channels.asgi
from django.conf import settings

if settings.DEBUG:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings.base")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings.production")
channel_layer = channels.asgi.get_channel_layer()
