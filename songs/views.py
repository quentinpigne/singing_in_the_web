from django.shortcuts import render
from django.http.response import JsonResponse
from songs.models import Artist, Album, Song

def index(request):
    return render(request, 'songs/index.html')

def search(request):
    all_art = Artist.objects.filter(artist_name__icontains=request.GET['query'])
    all_alb = Album.objects.filter(album_name__icontains=request.GET['query'])
    all_songs = Song.objects.filter(title__icontains=request.GET['query'])
    
    art = []
    alb = []
    songs = []

    i = 0
    while len(art) + len(alb) + len(songs) < 9 and i < 9:
        if i < len(all_art):
            art.append(all_art[i])
        if i < len(all_alb) and len(art) + len(alb) + len(songs) < 9:
            alb.append(all_alb[i])
        if i < len(all_songs) and len(art) + len(alb) + len(songs) < 9:
            songs.append(all_songs[i])
        i = i+1
    
    j = {}
    j['nodes'] = []
    for a in art:
        j['nodes'].append({'name': a.artist_name, 'type': 0})
    for a in alb:
        j['nodes'].append({'name': a.album_name, 'type': 1})
    for s in songs:
        j['nodes'].append({'name': s.title, 'type': 2})

    return JsonResponse(j)

def artist_details(request):
    art = Artist.objects.get(artist_name=request.GET['name'])

    j = {}
    j['artist_familiarity'] = art.artist_familiarity
    j['artist_hotness'] = art.artist_hotness
    j['artist_latitude'] = art.artist_latitude
    j['artist_longitude'] = art.artist_longitude
    j['artist_location'] = art.artist_location

    return JsonResponse(j)