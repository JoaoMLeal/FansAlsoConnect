from django.db import models


# Create your models here.
class Artist(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=100)
    related_artists = models.ManyToManyField('self')
