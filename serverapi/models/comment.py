""" Comment model for Mockingbird """

from django.db import models
from rest_framework.authtoken.models import Token

class Comment(models.Model):

    author= models.ForeignKey(Token, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True, auto_now_add=False)
    comment_edited = models.BooleanField(default=False)
    voice = models.ForeignKey("Voice", on_delete=models.CASCADE)
    comment_detail = models.CharField(max_length= 250)
