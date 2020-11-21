from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from playlists.models import Groups, Song, Playlist, Genre, Album, Singer


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = '__all__'


class SongSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(max_length=200, source='group.name', default=None)
    genre_name = serializers.CharField(max_length=200, source='genre.name', default=None)
    album_name = serializers.CharField(max_length=200, source='album.name', default=None)
    singer_name = serializers.CharField(max_length=200, source='singer.full_name', default=None)

    class Meta:
        model = Song
        fields = ('name', 'group_name', 'genre_name', 'album_name', 'singer_name', 'source')

    def __init__(self, *args, **kwargs):
        self.user = None
        self.group = None
        if kwargs.get('user'):
            self.user = kwargs.pop('user')

        super().__init__(**kwargs)

    def create(self, validated_data):
        group, created = Groups.objects.get_or_create(name=validated_data['group']['name'])
        genre, created = Genre.objects.get_or_create(name=validated_data['genre']['name'])
        album, created = Album.objects.get_or_create(name=validated_data['album']['name'], group=group)
        singer, created = Singer.objects.get_or_create(full_name=validated_data['singer']['full_name'], group=group)
        song = Song.objects.create(name=validated_data['name'],
                                   group=group,
                                   genre=genre,
                                   album=album,
                                   singer=singer,
                                   source=validated_data['source'],
                                   manager=self.user)

        return song

    def update(self, instance: Song, validated_data):
        if not instance.manager == self.user:
            raise ValueError('This song did not created by user')
        else:
            group, created = Groups.objects.get_or_create(name=validated_data['group']['name'])
            genre, created = Genre.objects.get_or_create(name=validated_data['genre']['name'])
            album, created = Album.objects.get_or_create(name=validated_data['album']['name'], group=group)
            singer, created = Singer.objects.get_or_create(full_name=validated_data['singer']['full_name'], group=group)

            instance.name = validated_data['name']
            instance.group = group
            instance.genre = genre
            instance.album = album
            instance.singer = singer
            instance.source = validated_data['source']
            instance.save()
            return instance


class SongToPlaylistSerializer(PrimaryKeyRelatedField, SongSerializer):
    pass


class PlaylistSerializer(serializers.ModelSerializer):
    songs = SongToPlaylistSerializer(many=True, queryset=Song.objects.all())

    class Meta:
        model = Playlist
        fields = ('name', 'songs')

    def __init__(self, *args, **kwargs):
        self.user = None
        if kwargs.get('user'):
            self.user = kwargs.pop('user')

        super().__init__(**kwargs)

    def create(self, validated_data):

        playlist = Playlist.objects.create(name=validated_data['name'],
                                           user=self.user)

        for song in validated_data['songs']:
            playlist.songs.add(song)

        return playlist

    def update(self, instance: Playlist, validated_data):
        if not instance.user == self.user:
            raise ValueError('Playlist is not this user!')
        instance.name = validated_data['name']
        for song in validated_data['songs']:
            instance.songs.add(song)
        instance.save()
        return instance


class PlaylistGETSerializer(PlaylistSerializer):
    songs = serializers.StringRelatedField(many=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
