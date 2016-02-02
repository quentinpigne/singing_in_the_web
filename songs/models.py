#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.fields.related import ForeignKey


class Album(models.Model):
    album_id = models.AutoField(primary_key=True)
    album_name = models.CharField(max_length=1024, verbose_name='Titre')
    album_year = models.IntegerField(blank=True, null=True, verbose_name='Année de sortie')
    album_7digitalid = models.IntegerField(blank=True, null=True, verbose_name='Identifiant 7digital')
    songs = models.ManyToManyField('Song', verbose_name='Chansons')
    
    def __unicode__ (self):
        return self.album_name

    class Meta:
        db_table = 'Album'
        verbose_name='Album'


class Artist(models.Model):
    artist_id = models.CharField(max_length=32, primary_key=True, verbose_name='Identifiant')
    artist_mbid = models.CharField(max_length=40, blank=True, null=True, verbose_name='Identifiant Musicbrainz')
    artist_playmeid = models.IntegerField(blank=True, null=True, verbose_name='Identifiant Playme')
    artist_name = models.CharField(max_length=1024, verbose_name='Nom')
    artist_familiarity = models.FloatField(blank=True, null=True, verbose_name='Popularité')
    artist_hotness = models.FloatField(blank=True, null=True, verbose_name='Hotness')
    artist_latitude = models.FloatField(blank=True, null=True, verbose_name='Latitude')
    artist_longitude = models.FloatField(blank=True, null=True, verbose_name='Longitude')
    artist_location = models.CharField(max_length=1024, blank=True, null=True, verbose_name='Localisation')
    artist_7digitalid = models.IntegerField(blank=True, null=True, verbose_name='Identifiant 7digital')
    similar_artists = models.ManyToManyField('Artist', blank=True, verbose_name='Artistes similaires')
    songs = models.ManyToManyField('Song', blank=True, verbose_name='Chansons')
    
    def __unicode__ (self):
        return self.artist_name
    
    class Meta:
        db_table = "Artist"
        verbose_name='Artiste'


class Artistterm(models.Model):
    term_id = models.AutoField(primary_key=True)
    artist = models.ForeignKey('Artist')
    term = models.CharField(max_length=40)
    terms_freq = models.FloatField()
    terms_weight = models.FloatField()
    
    def __unicode__ (self):
        return self.term

    class Meta:
        db_table = 'ArtistTerm'


class Musicbrainztag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    artist = models.ForeignKey('Artist')
    tag = models.CharField(max_length=255)
    tag_count = models.IntegerField()
    
    def __unicode__ (self):
        return self.tag

    class Meta:
        db_table = 'MusicBrainzTag'


class Song(models.Model):
    song_id = models.CharField(primary_key=True, max_length=32, verbose_name='Identifiant')
    track_id = models.CharField(max_length=32, verbose_name='Autre identifiant')
    title = models.CharField(max_length=1024, verbose_name='Titre')
    num_songs = models.IntegerField(blank=True, null=True, verbose_name='Nombre de chansons')
    track_7digitalid = models.IntegerField(blank=True, null=True, verbose_name='Indentifaint 7digital')
    song_hotness = models.FloatField(blank=True, null=True, verbose_name='Hotness')
    similar_songs = models.ManyToManyField('Song', through='Similarity', blank=True, verbose_name='Chansons similaires')
    
    def __unicode__ (self):
        return self.title

    class Meta:
        db_table = 'Song'
        verbose_name='Chanson'


class Songstatistic(models.Model):
    song_stats_id = models.AutoField(primary_key=True)
    song = models.ForeignKey('Song')
    analysis_sample_rate = models.CharField(max_length=40, blank=True, null=True)
    audio_md5 = models.CharField(max_length=32, blank=True, null=True)
    danceability = models.FloatField(blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    end_of_fade_in = models.FloatField(blank=True, null=True)
    energy = models.FloatField(blank=True, null=True)
    key_item = models.IntegerField(blank=True, null=True)
    key_confidence = models.FloatField(blank=True, null=True)
    loudness = models.FloatField(blank=True, null=True)
    mode = models.IntegerField(blank=True, null=True)
    mode_confidence = models.FloatField(blank=True, null=True)
    start_of_fade_out = models.FloatField(blank=True, null=True)
    tempo = models.FloatField(blank=True, null=True)
    time_signature = models.IntegerField(blank=True, null=True)
    time_signature_confidence = models.FloatField(blank=True, null=True)
    other_stats = models.BinaryField(blank=True, null=True)
    
    def __unicode__ (self):
        return self.duration

    class Meta:
        db_table = 'SongStatistic'


class Listening(models.Model):
    listener = ForeignKey('Listener')
    song = ForeignKey('Song')
    nb_listening = models.IntegerField()
    
    class Meta:
        db_table = 'Listening'


class Listener(models.Model):
    listener_id = models.CharField(primary_key=True, max_length=40)
    songs = models.ManyToManyField('Song', through='Listening', blank=True)
    
    def __unicode__ (self):
        return self.listener_id

    class Meta:
        db_table = 'Listener'
        
class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=255)
    tag_count = models.IntegerField()
    songs = models.ManyToManyField('Song')
    
    
    def __unicode__ (self):
        return self.tag

    class Meta:
        db_table = 'Tag'    
        
class Similarity(models.Model):
    song1 = ForeignKey('Song', related_name='%(class)s_similarity_song1', verbose_name='Chanson')
    song2 = ForeignKey('Song', related_name='%(class)s_similarity_song2', verbose_name='Chanson')
    similarity = models.FloatField()
    
    class Meta:
        db_table = 'Similarity'
        verbose_name = 'Chansons Similaire'