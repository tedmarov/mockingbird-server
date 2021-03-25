""" Comment model for Mockingbird """

from django.db import models

class Comment(models.Model):

    text_title = models.CharField(max_length= 50)
    text_body = models.CharField(max_length= 250)
    text_source = models.CharField(max_length= 250)
    text_edited = models.DateTimeField(auto_now=True, auto_now_add=False)