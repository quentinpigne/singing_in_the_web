from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http.response import JsonResponse
from songs.models import Artist, Album, Song, Songstatistic

def index(request):
    return render(request, 'songs/index.html')

def search(request):
    if request.GET['query'] == "":
        return JsonResponse({'nodes': []})

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
        j['nodes'].append({'id': a.artist_id, 'name': a.artist_name, 'type': 0})
    for a in alb:
        j['nodes'].append({'id': a.album_id, 'name': a.album_name, 'type': 1})
    for s in songs:
        j['nodes'].append({'id': s.song_id, 'name': s.title, 'type': 2})

    return JsonResponse(j)

def artist_details(request):
    try:
        art = Artist.objects.get(artist_id=request.GET['artist_id'])
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
        song = Song.objects.get(song_id=request.GET['song_id'])
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
        alb = Album.objects.get(album_id=request.GET['album_id'])
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'L\'album n\'existe pas'})
    
    j = {}
    j['album_year'] = alb.album_year
    
    return JsonResponse(j)

def artist_relatives(request):
    try: 
        art = Artist.objects.get(artist_id=request.GET['artist_id'])
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'L\'artiste n\'existe pas'})
    
    all_sim_art = art.similar_artists.all()
    all_songs = art.songs.all()
    
    sim_art = []
    songs = []

    i = 0
    while len(sim_art) + len(songs) < 8 and i < 8:
        if i < len(all_sim_art):
            sim_art.append(all_sim_art[i])
        if i < len(all_songs) and len(sim_art) + len(songs) < 8:
            songs.append(all_songs[i])
        i = i+1
    
    j = {}
    j['nodes'] = []
    for a in sim_art:
        j['nodes'].append({'name': a.artist_name, 'type': 0})
    for s in songs:
        j['nodes'].append({'name': s.title, 'type': 2})
         
    return JsonResponse(j)

def song_relatives(request):
    try: 
        song = Song.objects.get(song_id=request.GET['song_id'])
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'La chanson n\'existe pas'})
    
    all_sim_songs = song.similar_songs.all()
    all_art = song.artist_set.all()
    all_alb = song.album_set.all()
    
    sim_songs = []
    art = []
    alb = []

    i = 0
    while len(art) + len(alb) + len(sim_songs) < 9 and i < 9:
        if i < len(all_art):
            art.append(all_art[i])
        if i < len(all_alb) and len(art) + len(alb) + len(sim_songs) < 9:
            alb.append(all_alb[i])
        if i < len(all_sim_songs) and len(art) + len(alb) + len(sim_songs) < 9:
            sim_songs.append(all_sim_songs[i])
        i = i+1
    
    j = {}
    j['nodes'] = []
    for a in art:
        j['nodes'].append({'name': a.artist_name, 'type': 0})
    for a in alb:
        j['nodes'].append({'name': a.album_name, 'type': 1})
    for s in sim_songs:
        j['nodes'].append({'name': s.title, 'type': 2})

    return JsonResponse(j)

def album_relatives(request):
    try: 
        alb = Album.objects.get(album_id=request.GET['album_id'])
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'L\'album n\'existe pas'})
    
    all_songs = alb.songs.all()
    
    songs = []

    i = 0
    while len(songs) < 8 and i < 8:
        if i < len(all_songs) and len(songs) < 8:
            songs.append(all_songs[i])
        i = i+1
    
    j = {}
    j['nodes'] = []
    for s in songs:
        j['nodes'].append({'name': s.title, 'type': 2})
         
    return JsonResponse(j)