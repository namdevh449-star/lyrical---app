from django.contrib import admin
from .models import Song, Album, Playlist

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'mood')
    readonly_fields = ('mood',)

admin.site.register(Album)
admin.site.register(Playlist)