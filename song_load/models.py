from django.db import models
from django.utils import timezone

class User(models.Model):
    user_name = models.CharField(max_length=200, unique=True)
    date_added_to_db = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user_name

class Artist(models.Model):
    artist_name = models.CharField(max_length=200)
    artist_id = models.CharField(max_length=200, unique=True)
    date_added_to_db = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.artist_name

class Album(models.Model):
    album_id = models.CharField(max_length=200, unique=True)
    album_name = models.CharField(max_length=200, default="album")
    image_url = models.CharField(max_length=200, default="url")
    artist = models.ForeignKey(Artist, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.album_name

# Create your models here.
class Song(models.Model):
    artists = models.ManyToManyField(Artist)
    song_name = models.CharField(max_length=200)
    song_id = models.CharField(max_length=200, unique=True)
    song_length = models.IntegerField()
    album = models.ForeignKey(Album, null=True, on_delete=models.PROTECT)
    users_added = models.ManyToManyField(User)
    date_added_to_lib = models.DateTimeField(default=timezone.now)
    date_added_to_db = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.song_name

    def artist_count(self):
        return len(self.artists)
