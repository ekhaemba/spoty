import sys
import spotipy
import spotipy.util as util
from pprint import pprint
import os
import django
from django.db import IntegrityError
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spotmy_app.settings")
django.setup()
from song_load.models import Song, User, Artist, Album
from spotipy_consts import REDIRECT_URI, CLIENT_ID, CLIENT_SECRET
scope = 'user-library-read'

def main(username):
    os.environ["SPOTIPY_CLIENT_ID"] = CLIENT_ID
    os.environ["SPOTIPY_CLIENT_SECRET"] = CLIENT_SECRET
    os.environ["SPOTIPY_REDIRECT_URI"] = REDIRECT_URI

    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        index = 0
        limit = 50
        offset = index*limit
        results = sp.current_user_saved_tracks(offset=offset, limit=limit)
        total = results['total']
        try:
            this_user = User(user_name=username)
            this_user.save()
        except IntegrityError as e:
            this_user = User.objects.all().get(user_name=username)


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
                    new_song = Song.objects.all().get(song_id=song_id)
                #Save the album and add this song to it
                try:
                    new_album.save()
                except IntegrityError as e:
                    new_album = Album.objects.all().get(album_id=album_id)
                new_album.song_set.add(new_song)
                new_song.users_added.add(this_user)
                #For all the artists add them to this song
                for ind, artist in enumerate(artists):
                    artist_id = artist['id']
                    artist_name = artist['name']
                    new_artist = Artist(artist_name=artist_name, artist_id=artist_id)
                    try:
                        new_artist.save()
                    except IntegrityError as e:
                        new_artist = Artist.objects.all().get(artist_id=artist_id)
                    if ind == 0:
                        new_artist.album_set.add(new_album)
                    new_song.artists.add(new_artist)
            index += 1
            offset = index*limit
            results = sp.current_user_saved_tracks(offset=offset, limit=limit)
    else:
        print("Can't get token for", username)

if __name__ =="__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
        main(username)
    else:
        print("Usage: {} username".format(sys.argv[0]))
        sys.exit()
