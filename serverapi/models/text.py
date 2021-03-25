""" Text model for Mockingbird """

from django.db import models

class Text(models.Model):

    text_title = models.CharField(max_length= 50)
    submitter = models.ForeignKey("Birdie", on_delete=models.CASCADE)
    edited_on = models.DateTimeField(auto_now=True, auto_now_add=False)
    text_body = models.CharField(max_length= 250)
    text_source = models.CharField(max_length= 250)