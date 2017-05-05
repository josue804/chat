from django.db import models
from autoslug import AutoSlugField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from chat.extras import get_local_time
from lazysignup.models import LazyUser

class GuestUser(models.Model):
    username = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True)
    temp_token = models.CharField(max_length=500)
    session_key = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.username

##Inherits full functionality from Django Use class
class CustomUser(AbstractUser):
    about = models.TextField(max_length=1000, blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True, upload_to='avatar')
    lazy_key = models.CharField(max_length=255, blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)

    hospital_location = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    topic_interests = models.TextField(blank=True, null=True)
    subscriptions = models.ManyToManyField('chat.Room', null=True, blank=True)

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def topics(self):
        return self.topic_interests.split(',')

    def get_address(self):
        return self.city + ', ' + self.state + ' ' + self.country

    def has_more_information(self):
        return not(not self.topic_interests and not self.subscriptions.all() and not self.about)

    def __str__(self):
        return self.username

    def get_username(self):
        try:
            LazyUser.objects.get(user__username=self.username)
            return self.nickname
        except:
            return self.username
