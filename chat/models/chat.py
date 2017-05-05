from django.db import models
from autoslug import AutoSlugField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from chat.extras import get_local_time
from .auth import CustomUser
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=255)
    connections = models.IntegerField(default=0)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name

    def add_connection(self):
        self.connections += 1
        self.save()

    def remove_connection(self):
        self.connections -= 1
        self.save()

    class Meta:
        ordering = ['name']

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages')
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=get_local_time, db_index=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    @property
    def formatted_timestamp(self):
        return timezone.localtime(self.timestamp).strftime('%b %-d %-I:%M %p PST')

    @property
    def formatted_handle(self):
        return mark_safe('<a href="' + reverse('account-detail', kwargs={'pk': self.user.pk}) + '" target="_blank">' + self.handle + '</a>' + ' on ' + timezone.localtime(self.timestamp).strftime('%b %-d %-I:%M %p PST'))
