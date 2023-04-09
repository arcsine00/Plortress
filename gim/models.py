from django.conf import settings
from django.db import models
from django.utils import timezone

class Request(models.Model):
    speech = models.CharField(max_length=20)
    bpm = models.IntegerField()
    beats = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)
    fname = models.CharField(max_length=50, null=True, blank=True)