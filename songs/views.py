from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http.response import JsonResponse
from songs.models import Artist, Album, Song, Songstatistic

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
    try:
        art = Artist.objects.get(artist_name=request.GET['artist_name'])
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'L\'artiste n\'existe pas'})

    j = {}
    j['artist_familiarity'] = art.artist_familiarity
    j['artist_hotness'] = art.artist_hotness
    j['artist_latitude'] = art.artist_latitude
    j['artist_longitude'] = art.artist_longitude
    j['artist_location'] = art.artist_location

    return JsonResponse(j)

def song_details(request):
    try: 
        song = Song.objects.get(title=request.GET['title'])
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'La chanson n\'existe pas'})
    
    j = {}
    j['song_hotness'] = song.song_hotness
    
    stats = Songstatistic.objects.get(song=song)
    
    j['analysis_sample_rate'] = stats.analysis_sample_rate
    j['audio_md5'] = stats.audio_md5
    j['danceability'] = stats.danceability
    j['duration'] = stats.duration
    j['end_of_fade_in'] = stats.end_of_fade_in
    j['energy'] = stats.energy
    j['key_item'] = stats.key_item
    j['key_confidence'] = stats.key_confidence
    j['loudness'] = stats.loudness
    j['mode'] = stats.mode
    j['mode_confidence'] = stats.mode_confidence
    j['start_of_fade_out'] = stats.start_of_fade_out
    j['tempo'] = stats.tempo
    j['time_signature'] = stats.time_signature
    j['time_signature_confidence'] = stats.time_signature_confidence
    
    return JsonResponse(j)

def album_details(request):
    try: 
        alb = Album.objects.get(album_name=request.GET['album_name'])
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'L\'album n\'existe pas'})
    
    j = {}
    j['album_year'] = alb.album_year
    
    return JsonResponse(j)