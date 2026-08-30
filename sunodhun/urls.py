from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('playlists/', views.playlists_view, name='playlists'),
    path('playlists/create/', views.create_playlist, name='create_playlist'),
    path('playlists/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('playlists/<int:playlist_id>/add/<int:song_id>/', views.add_song_to_playlist, name='add_song'),
    path('playlists/<int:playlist_id>/remove/<int:song_id>/', views.remove_song_from_playlist, name='remove_song'),
    path('play/<int:song_id>/', views.play_song, name='play_song'),
    path('analytics/', views.analytics_dashboard, name='analytics'),
    path('analytics/export/', views.export_analytics_csv, name='export_analytics_csv'),
    path('library/', views.library_view, name='library'),
    path('history/',views.history_view, name='history'),
    path('like/<int:song_id>/', views.toggle_like, name='toggle_like'),
    path('lyrics-timer/', views.lyrics_timer, name='lyrics_timer'),
]