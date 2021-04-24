from django.db import models
from rest_framework.authtoken.models import Token

class Text(models.Model):

    title = models.CharField(max_length=50)
    submitter = models.ForeignKey(Token, on_delete=models.CASCADE)
    body = models.CharField(max_length=250)
    source = models.CharField(max_length=250)