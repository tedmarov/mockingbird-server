""" Comment model for BirdieVoices """

from django.db import models
from rest_framework.authtoken.models import Token

class Comment(models.Model):

    author= models.ForeignKey(Token, on_delete=models.CASCADE)
    voice = models.ForeignKey("Voice", on_delete=models.CASCADE)
    content = models.CharField(max_length= 250)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=False)
