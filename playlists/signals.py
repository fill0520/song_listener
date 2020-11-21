from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from datetime import datetime

from playlists.models import Song, Playlist


@receiver(post_delete, sender=Song)
def delete_song(sender, instance: Song, *args, **kwargs):
    playlists = Playlist.objects.filter(songs__id = instance.id)
    for playlist in playlists:
        playlist.songs.remove(instance)

