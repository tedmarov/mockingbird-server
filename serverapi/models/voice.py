""" Mockingbird Voice model  """

from django.db import models

class Voice(models.Model):
    """ Model representation of a voice that any birdie can make """

    voice_name = models.CharField(max_length=45)
    date_created = models.DateField(auto_now_add=True, auto_now=False)
    creator = models.ForeignKey("Birdie", on_delete=models.CASCADE)
    category = models.ForeignKey("VoiceCategory", on_delete=models.CASCADE)
    voice_text = models.CharField(max_length=3000)
    last_edit = models.DateField(auto_now_add=True, auto_now=False)
    