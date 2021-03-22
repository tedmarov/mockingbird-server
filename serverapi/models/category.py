""" Category model for BirdieVoices """

from django.db import models

class Category(models.Model):
    comment_label = models.CharField(max_length=25)