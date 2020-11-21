from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from playlists.models import Groups, Song, Playlist, Genre, Album, Singer
from playlists.serializers import GroupSerializer, SongSerializer, PlaylistSerializer, PlaylistGETSerializer, \
    UserSerializer
from django_filters.rest_framework import DjangoFilterBackend


class GroupView(generics.ListCreateAPIView):
    queryset = Groups.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]


class SongView(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'group', 'genre', 'album', 'singer']

    def get(self, request, *args, **kwargs):
        playlist_id = request.query_params.get('playlist', None)
        filters = {}

        name = request.query_params.get('name', False)
        group = request.query_params.get('group', False)
        genre = request.query_params.get('genre', False)
        album = request.query_params.get('album', False)
        singer = request.query_params.get('singer', False)

        if name:
            filters['name__contains'] = name
        if group:
            filters['group'] = Groups.objects.filter(id=group).first()
        if genre:
            filters['genre'] = Genre.objects.filter(id=genre).first()
        if album:
            filters['album'] = Album.objects.filter(id=album).first()
        if singer:
            filters['singer'] = Singer.objects.filter(id=singer).first()

        if playlist_id:
            queryset = Song.objects.filter(playlist__id=playlist_id, **filters)
            if not Playlist.objects.filter(id=playlist_id, user=request.user).count():
                return Response({})
        else:
            queryset = Song.objects.filter(manager=request.user, **filters)

        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

    def post(self, request, **kwargs):
        serializer = SongSerializer(data=request.data, user=request.user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Song was created successfully!')
        else:
            return Response(serializer.errors)

    def put(self, request):
        song = Song.objects.filter(name=request.data.get('name'), manager=request.user).first()
        if not song:
            return Response('Song does not exists!')

        serializer = SongSerializer(instance=song, data=request.data, user=request.user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Song was updated successfully!')
        else:
            return Response(serializer.errors)


class SongDeleteView(SongView):

    def post(self, request, **kwargs):
        song = Song.objects.filter(name=request.data.get('name'), group__name=request.data.get('group_name'),
                                   manager=request.user).first()
        if not song:
            return Response('Song does not exists!')

        song.delete()
        return Response("Song deleted!")


class PlaylistView(APIView):
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Playlist.objects.filter(user=request.user)

        serializer = PlaylistGETSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, user=request.user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Playlist was created successfully!')
        else:
            return Response(serializer.errors)

    def put(self, request):
        playlist = Playlist.objects.filter(name=request.data.get('name'), user=request.user).first()
        if not playlist:
            return Response('Song does not exists!')

        serializer = self.serializer_class(instance=playlist, data=request.data, user=request.user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Playlist was updated successfully!')
        else:
            return Response(serializer.errors)


class PlaylistDeleteView(PlaylistView):

    def post(self, request):
        playlist = Playlist.objects.filter(name=request.data.get('name'), user=request.user).first()
        if not playlist:
            return Response('Playlist does not exists!')

        playlist.delete()
        return Response("Playlist deleted!")


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
