from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Song, Artist, Album

def index(request):
    all_songs = Song.objects.all().order_by('song_name')
    paginator = Paginator(all_songs, 50)
    page = request.GET.get('page')
    songs = paginator.get_page(page)
    context = {
        'songs': songs
    }
    return render(request, 'song_load/index.html', context)

def song(request, song_id):
    this_song = Song.objects.get(song_id=song_id)
    album = this_song.album
    context = {
        'song':this_song,
        'artists':this_song.artists.all(),
        'album': album
    }
    return render(request, 'song_load/song.html', context)

def artist(request, artist_id):
    this_artist = Artist.objects.get(artist_id=artist_id)
    songs_by_artist = this_artist.song_set.all()
    albums_by_artist = this_artist.album_set.all()
    context = {
        'artist':this_artist,
        'songs':songs_by_artist,
        'albums':albums_by_artist
    }
    return render(request, 'song_load/artist.html', context)

def album(request, album_id):
    this_album = Album.objects.get(album_id=album_id)
    this_artist = this_album.artist
    songs_by_album = this_album.song_set.all()
    context = {
        'album':this_album,
        'songs':songs_by_album,
        'artist':this_artist
    }
    return render(request, 'song_load/album.html', context)
