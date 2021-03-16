""" Comment model for Mockingbird """

from django.db import models
from rest_framework.authtoken.models import Token

class Comment(models.Model):

    comment_title = models.CharField(max_length= 50)
    author= models.ForeignKey(Token, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=False)
    voice = models.ForeignKey("Voice", on_delete=models.CASCADE)
    comment_detail = models.CharField(max_length= 250)
    last_edit = models.DateTimeField(auto_now=False, auto_now_add=False)