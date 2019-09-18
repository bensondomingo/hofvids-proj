from django.db import models

class Hall(models.Model):
    title = models.CharField(max_length=255)

class Video(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.URLField()
    youtube_id = models.CharField(max_length=255)