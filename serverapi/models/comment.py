""" Comment model for Mockingbird """

from django.db import models

class Comment(models.Model):

    comment_title = models.CharField(max_length= 50)
    author= models.ForeignKey("Birdie", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True, auto_now_add=False)
    voice = models.ForeignKey("Voice", on_delete=models.CASCADE)
    comment_detail = models.CharField(max_length= 250)
    comment_edited = models.DateTimeField(auto_now=True, auto_now_add=False)