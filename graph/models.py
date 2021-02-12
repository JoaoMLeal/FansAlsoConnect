from django.db import models


class AudioNode(models.Model):
    artist_id = models.TextField()
    artist_name = models.TextField()
# Create your models here.
