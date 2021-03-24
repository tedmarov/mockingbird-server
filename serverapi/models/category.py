""" Category model for BirdieVoices """

from django.db import models

class Category(models.Model):
    category_label = models.CharField(max_length=25)