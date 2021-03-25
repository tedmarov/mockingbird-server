""" Mockingbird Birdie model  """

from django.db import models
from django.conf import settings

class BirdieText(models.Model):
    """ Model representation of a birdie account that can be created """

    birdie = models.ForeignKey("Birdie", on_delete=models.CASCADE)
    text = models.ForeignKey("Text", on_delete=models.CASCADE)

    # @property
    # def full_name(self):
    #     """Provides full name for a user

    #     Returns:
    #         string: Full name of user
    #     """
    #     return f"{self.user.first_name} {self.user.last_name}"
    