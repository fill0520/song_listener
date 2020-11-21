from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from playlists import views

urlpatterns = [
    path('groups/', views.GroupView.as_view()),
    path('songs/', views.SongView.as_view()),
    path('playlists/', views.PlaylistView.as_view()),
    path('delete_playlist/', views.PlaylistDeleteView.as_view()),
    path('delete_song/', views.SongDeleteView.as_view()),
    path('registration/', views.UserCreate.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)