from django.db import models
from autoslug import AutoSlugField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from chat.extras import get_local_time

class GuestUser(models.Model):
    username = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True)
    temp_token = models.CharField(max_length=500)
    ip_address = models.GenericIPAddressField(null=True)

    def __str__(self):
        return self.username

##Inherits full functionality from Django Use class
class CustomUser(AbstractUser):
    about = models.TextField(max_length=1000, blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True, upload_to='avatar')

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.username
