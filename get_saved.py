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
from song_load.models import Song, User

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
    print(results['items'][0])
    try:
        new_user = User(user_name=username)
        new_user.save()
    except IntegrityError as e:
        print("User already exists")
    artist_counter = Counter()
    while offset < total:
        for item in results['items']:
            track = item['track']
            artist_id = track['artists'][0]['id']
            artist_name = track['artists'][0]['name']
            song_name = track['name']
            song_id = track['id']
            song_length = track['duration_ms']
            date_added_to_lib = item['added_at']
            new_song = Song(artist_name=artist_name,song_name=song_name,song_id=song_id,song_length=song_length,date_added_to_lib=date_added_to_lib)
            print(new_song)
            try:
                new_song.save()
            except IntegrityError as e:
                print("Song already exists: {}".format(new_song))
        index += 1
        offset = index*limit
        results = sp.current_user_saved_tracks(offset=offset, limit=limit)

    # top_list = artist_counter.most_common(AMOUNT_OF_TOP)
    # labels, ys = zip(*top_list)
    # s = pd.Series(ys,labels)
    # plt.title('Top {} Songs in your saved library'.format(AMOUNT_OF_TOP))
    # plt.ylabel('Number of Songs')
    # plt.xlabel('Artist')
    # s.plot(kind='bar',colormap='Accent')
    # plt.show()
else:
    print("Can't get token for", username)
