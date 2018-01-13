from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('song/<str:song_id>', views.song, name="song info"),
    path('artist/<str:artist_id>', views.artist, name="artist info"),
    path('album/<str:album_id>', views.album, name="album info")
]
