from __future__ import unicode_literals

from django.db import models
from django.db.models.fields.related import ForeignKey


class Albums(models.Model):
    album_id = models.AutoField(primary_key=True)
    album_name = models.CharField(max_length=1024)
    album_year = models.IntegerField(blank=True, null=True)
    album_7digitalid = models.IntegerField(blank=True, null=True)
    songs = models.ManyToManyField('Songs')

    class Meta:
        db_table = 'Albums'


class Artists(models.Model):
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
    similar_artists = models.ManyToManyField('Artists')
    songs = models.ManyToManyField('Songs')
    
    class Meta:
        db_table = "Artists"


class Artistterms(models.Model):
    term_id = models.AutoField(primary_key=True)
    artist = models.ForeignKey('Artists')
    term = models.CharField(max_length=40)
    terms_freq = models.DecimalField(max_digits=16, decimal_places=15)
    terms_weight = models.FloatField()

    class Meta:
        db_table = 'ArtistTerms'


class Musicbrainztags(models.Model):
    tag_id = models.AutoField(primary_key=True)
    artist = models.ForeignKey('Artists')
    tag = models.CharField(max_length=40)
    tag_count = models.IntegerField()

    class Meta:
        db_table = 'MusicBrainzTags'


class Songs(models.Model):
    song_id = models.CharField(primary_key=True, max_length=32)
    title = models.CharField(max_length=1024)
    num_songs = models.IntegerField(blank=True, null=True)
    track_id = models.CharField(max_length=32, blank=True, null=True)
    track_7digitalid = models.IntegerField(blank=True, null=True)
    song_hotness = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'Songs'


class Songsstatistics(models.Model):
    song_stats_id = models.AutoField(primary_key=True)
    song = models.ForeignKey('Songs')
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

    class Meta:
        db_table = 'SongsStatistics'


class Listening(models.Model):
    listener = ForeignKey('Listeners')
    song = ForeignKey('Songs')
    nb_listening = models.IntegerField()
    
    class Meta:
        db_table = 'Listening'


class Listeners(models.Model):
    listener_id = models.CharField(primary_key=True, max_length=40)
    songs = models.ManyToManyField('Songs', through='Listening')

    class Meta:
        db_table = 'Listeners'