from django.db import models

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=300)

class Movie(models.Model):
    title = models.CharField(max_length=300)
    release_date = models.DateField()
    overview = models.TextField()
    vote_average = models.FloatField()
    genres = models.ManyToManyField(Genre)
    poster_path = models.CharField(max_length=300)