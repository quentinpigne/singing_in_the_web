from __future__ import unicode_literals

from django.db import models
from django.db.models.fields.related import ForeignKey


class Album(models.Model):
    album_id = models.AutoField(primary_key=True)
    album_name = models.CharField(max_length=1024)
    album_year = models.IntegerField(blank=True, null=True)
    album_7digitalid = models.IntegerField(blank=True, null=True)
    songs = models.ManyToManyField('Song')
    
    def __unicode__ (self):
        return self.album_name

    class Meta:
        db_table = 'Album'


class Artist(models.Model):
    artist_id = models.CharField(max_length=32, primary_key=True)
    artist_mbid = models.CharField(max_length=40)
    artist_playmeid = models.IntegerField()
    artist_name = models.CharField(max_length=1024)
    artist_familiarity = models.FloatField(blank=True, null=True)
    artist_hotness = models.FloatField(blank=True, null=True)
    artist_latitude = models.FloatField(blank=True, null=True)
    artist_longitude = models.FloatField(blank=True, null=True)
    artist_location = models.CharField(max_length=1024, blank=True, null=True)
    artist_7digitalid = models.IntegerField()
    similar_artists = models.ManyToManyField('Artist')
    songs = models.ManyToManyField('Song')
    
    def __unicode__ (self):
        return self.artist_name
    
    class Meta:
        db_table = "Artist"


class Artistterm(models.Model):
    term_id = models.AutoField(primary_key=True)
    artist = models.ForeignKey('Artist')
    term = models.CharField(max_length=40)
    terms_freq = models.DecimalField(max_digits=16, decimal_places=15)
    terms_weight = models.FloatField()
    
    def __unicode__ (self):
        return self.term

    class Meta:
        db_table = 'ArtistTerm'


class Musicbrainztag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    artist = models.ForeignKey('Artist')
    tag = models.CharField(max_length=40)
    tag_count = models.IntegerField()
    
    def __unicode__ (self):
        return self.tag

    class Meta:
        db_table = 'MusicBrainzTag'


class Song(models.Model):
    song_id = models.CharField(primary_key=True, max_length=32)
    title = models.CharField(max_length=1024)
    num_songs = models.IntegerField(blank=True, null=True)
    track_id = models.CharField(max_length=32, blank=True, null=True)
    track_7digitalid = models.IntegerField(blank=True, null=True)
    song_hotness = models.FloatField(blank=True, null=True)
    similar_songs = models.ManyToManyField('Song', through='Similarity')
    
    def __unicode__ (self):
        return self.title

    class Meta:
        db_table = 'Song'


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
    songs = models.ManyToManyField('Song', through='Listening')
    
    def __unicode__ (self):
        return self.listener_id

    class Meta:
        db_table = 'Listener'
        
class Word(models.Model):
    track_id = models.ForeignKey('Song')
    mxm_tid = models.IntegerField()
    word = models.CharField(max_length=40)
    count = models.IntegerField()
    
    
    def __unicode__ (self):
        return self.word

    class Meta:
        db_table = 'Word'    
        
class Similarity(models.Model):
    song1 = ForeignKey('Song', related_name='%(class)s_similarity_song1')
    song2 = ForeignKey('Song', related_name='%(class)s_similarity_song2')
    similarity = models.DecimalField(max_digits=19, decimal_places=18)
    
    class Meta:
        db_table = 'Similarity'