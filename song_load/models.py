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
# Create your models here.
class Song(models.Model):
    main_artist = models.ForeignKey(Artist, on_delete=models.PROTECT)
    features = models.ManyToManyField(Artist)
    song_name = models.CharField(max_length=200)
    song_id = models.CharField(max_length=200, unique=True)
    artist_id = models.CharField(max_length=200)
    song_length = models.IntegerField()
    users_added = models.ManyToManyField(User)
    date_added_to_lib = models.DateTimeField(default=timezone.now)
    date_added_to_db = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} - {}".format(self.main_artist, self.song_name)
