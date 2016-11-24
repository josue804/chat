from django.db import models
from autoslug import AutoSlugField
from django.utils import timezone

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages')
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __str__(self):
        return self.message

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')

    @property
    def formatted_handle(self):
        return self.handle + ' on ' + self.timestamp.strftime('%b %-d %-I:%M %p')
