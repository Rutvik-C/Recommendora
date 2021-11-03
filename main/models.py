from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Genre(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type


class Movie(models.Model):
    title = models.CharField(max_length=200)
    image_url = models.CharField(max_length=250)
    trailer_link = models.CharField(max_length=50)
    year = models.CharField(max_length=15)
    duration = models.CharField(max_length=20)
    language = models.CharField(max_length=200)
    description = models.CharField(max_length=450)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    production_company = models.CharField(max_length=150)
    actors = models.ManyToManyField(Actor)
    directors = models.ManyToManyField(Director)
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title
