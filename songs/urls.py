from django.conf.urls import url

from . import views

app_name = 'songs'
urlpatterns = [
    url(r'^search/$', views.search, name='search'),
    url(r'^artist_details/$', views.artist_details, name='artist_details'),
    url(r'^song_details/$', views.song_details, name='song_details'),
    url(r'^album_details/$', views.album_details, name='album_details'),
    url(r'^artist_relatives/$', views.artist_relatives, name='arist_relatives'),
    url(r'^song_relatives/$', views.song_relatives, name='song_relatives'),
    url(r'^album_relatives/$', views.album_relatives, name='album_relatives')
]