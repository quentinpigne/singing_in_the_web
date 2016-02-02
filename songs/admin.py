#-*- coding: utf-8 -*-
from django.contrib import admin
from songs.models import Album, Artist, Similarity, Song, Songstatistic

class AlbumAdmin(admin.ModelAdmin):
    exclude = ('album_id', )
    fieldsets = (
                (None, {
                        'fields': ('album_name', 'songs')
                        }
                 ),
                ('Autres propriétés', {
                                       'classes': ('collapse', ), 'fields': ('album_year', 'album_7digitalid') 
                                       }
                 
                 )
                )

class ArtistAdmin(admin.ModelAdmin):
    fieldsets = (
                 (None, {
                         'fields': ('artist_id', 'artist_name', 'songs')
                         }
                  ),
                 ('Autres informations', {
                                       'classes': ('collapse', ), 'fields': ('artist_familiarity', 'artist_hotness', 'artist_latitude', 'artist_longitude', 'artist_location', 'similar_artists') 
                                       }
                 
                 ),
                 ('Identifiants', {
                                   'classes': ('collapse', ), 'fields': ('artist_mbid', 'artist_playmeid', 'artist_7digitalid')
                                   }
                  
                  )
                 )
    
class SimilarityInline(admin.TabularInline):
    model = Similarity
    fk_name = 'song1'
    extra = 1
        
class SongAdmin(admin.ModelAdmin):
    fieldsets = (
                 (
                  None, {
                         'fields': ('song_id', 'track_id', 'title')
                         }
                  ),
                 ('Autres informations', {
                                          'classes': ('collapse', ), 'fields': ('num_songs', 'track_7digitalid', 'song_hotness')
                                          })
                 )
    inlines = (SimilarityInline, )

# Register your models here.
admin.site.register(Album, AlbumAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Song, SongAdmin)  
