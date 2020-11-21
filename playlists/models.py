from django.contrib.auth.models import User
from django.db import models


class Groups(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)


class Album(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Groups, on_delete=models.SET_NULL, default=None, null=True)


class Singer(models.Model):
    full_name = models.CharField(max_length=200)
    group = models.ForeignKey(Groups, on_delete=models.SET_NULL, default=None, null=True)


class Song(models.Model):
    name = models.CharField(max_length=200)
    group = models.ForeignKey(Groups, on_delete=models.SET_NULL, default=None, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, default=None, null=True)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, default=None, null=True)
    singer = models.ForeignKey(Singer, on_delete=models.SET_NULL, default=None, null=True)
    source = models.FileField()
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)

    def __str__(self):
        return f"{self.name} ({self.group})"

    class Meta:
        unique_together = ('name', 'group',)


class Playlist(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    songs = models.ManyToManyField(Song)
