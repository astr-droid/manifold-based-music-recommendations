# recommender/models.py
from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    track_id = models.CharField(max_length=64, unique=True)
    track_name = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="songs")

    danceability = models.FloatField()
    energy = models.FloatField()
    acousticness = models.FloatField()
    instrumentalness = models.FloatField()
    tempo = models.FloatField()
    valence = models.FloatField()

    embedding_x = models.FloatField()
    embedding_y = models.FloatField()

    def __str__(self):
        return f"{self.track_name} - {self.artist.name}"