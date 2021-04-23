from django.db import models
from rest_framework.authtoken.models import Token

class Voice(models.Model):
    """ Model representation of a voice that any birdie can make """

    name = models.CharField(max_length=45)
    created = models.DateField(auto_now_add=True, auto_now=False)
    recording = models.CharField(max_length=3000)
    edited = models.BooleanField()
    privacy = models.BooleanField()
    creator =  models.ForeignKey(Token, on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    text = models.ForeignKey("Text", on_delete=models.CASCADE)

