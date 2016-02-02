from django.contrib import admin
from songs.models import Album, Artist, Artistterm, Listener, Musicbrainztag, Song, Songstatistic, Tag

# Register your models here.
admin.site.register(Album)
admin.site.register(Artist)
admin.site.register(Artistterm)
admin.site.register(Listener)
admin.site.register(Musicbrainztag)
admin.site.register(Song)
admin.site.register(Songstatistic)
admin.site.register(Tag)