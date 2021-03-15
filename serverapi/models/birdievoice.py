""" Dreamcatcher User Model  """

from django.db import models

class BirdieVoice(models.Model):
    """ Model representation of the many voices a birdie can make """

    voice = models.ForeignKey("Voice", on_delete=models.CASCADE)
    birdie = models.ForeignKey("Birdie", on_delete=models.CASCADE)
