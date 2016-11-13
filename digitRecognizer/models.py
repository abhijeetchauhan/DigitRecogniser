from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Digit(models.Model):
  image = models.ImageField(upload_to = 'pic_folder/')
  result = models.IntegerField()
  correct = models.BooleanField()