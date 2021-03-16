""" VoiceCategory model for BirdieVoices """

from django.db import models

class VoiceCategory(models.Model):
    label = models.CharField(max_length=25)