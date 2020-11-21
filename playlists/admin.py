from django.contrib import admin

from playlists.models import Groups, Song, Playlist, Genre


@admin.register(Genre)
class GenresAdmin(admin.ModelAdmin):
    pass


@admin.register(Groups)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    pass


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    pass
