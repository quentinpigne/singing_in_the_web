from django.conf.urls import url

from . import views

app_name = 'songs'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^artist_details/$', views.artist_details, name='artist_detail'),
    url(r'^song_details/$', views.song_details, name='song_detail'),
    url(r'^album_details/$', views.album_details, name='album_detail'),
]