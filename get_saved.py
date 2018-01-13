import sys
import spotipy
import spotipy.util as util
from pprint import pprint
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import os
import django
from django.db import IntegrityError
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spotmy_app.settings")
django.setup()
from song_load.models import Song, User, Artist, Album

scope = 'user-library-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: {} username".format(sys.argv[0]))
    sys.exit()

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    index = 0
    limit = 50
    offset = index*limit
    results = sp.current_user_saved_tracks(offset=offset, limit=limit)
    total = results['total']
    try:
        new_user = User(user_name=username)
        new_user.save()
    except IntegrityError as e:
        print("User already exists")

    artist_counter = Counter()
    while offset < total:
        for item in results['items']:
            track = item['track']
            album_obj = track['album']
            #Artists
            artists = track['artists']
            #Song
            song_name = track['name']
            song_id = track['id']
            song_length = track['duration_ms']
            date_added_to_lib = item['added_at']
            #Album
            image_url = album_obj['images'][1]['url']
            album_name = album_obj['name']
            album_id = album_obj['id']

            new_song = Song(song_name=song_name, song_id=song_id,song_length=song_length, date_added_to_lib=date_added_to_lib)
            new_album = Album(album_id=album_id, image_url=image_url, album_name=album_name)
            #Save the song
            try:
                new_song.save()
            except IntegrityError as e:
                print("Song already exists: {}".format(new_song))
                new_song = Song.objects.all().get(song_id=song_id)
            #Save the album and add this song to it
            try:
                new_album.save()
            except IntegrityError as e:
                print("Album already exists: {}".format(new_album))
                new_album = Album.objects.all().get(album_id=album_id)
            new_album.song_set.add(new_song)
            #For all the artists add them to this song
            for ind, artist in enumerate(artists):
                artist_id = artist['id']
                artist_name = artist['name']
                new_artist = Artist(artist_name=artist_name, artist_id=artist_id)
                try:
                    new_artist.save()
                except IntegrityError as e:
                    print("Artist already exists: {}".format(new_artist))
                    new_artist = Artist.objects.all().get(artist_id=artist_id)
                if ind == 0:
                    new_artist.album_set.add(new_album)
                new_song.artists.add(new_artist)
            print(new_song)
        index += 1
        offset = index*limit
        results = sp.current_user_saved_tracks(offset=offset, limit=limit)

else:
    print("Can't get token for", username)
