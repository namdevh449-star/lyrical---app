import csv
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Song, Playlist, LikedSong, ListeningHistory
@login_required
def home(request):
    query = request.GET.get('q', '')
    if query:
        songs = Song.objects.filter(title__icontains=query) | \
                Song.objects.filter(artist__icontains=query) | \
                Song.objects.filter(mood__icontains=query) | \
                Song.objects.filter(language__icontains=query)
    else:
        songs = Song.objects.all()
    return render(request, 'home.html', {'songs': songs, 'query': query})
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')
@login_required
def playlists_view(request):
    playlists = Playlist.objects.filter(user=request.user)
    return render(request, 'playlists.html', {'playlists': playlists})


@login_required
def create_playlist(request):
    if request.method == 'POST':
        name = request.POST['name']
        Playlist.objects.create(user=request.user, name=name)
    return redirect('playlists')


@login_required
def playlist_detail(request, playlist_id):
    playlist = Playlist.objects.get(id=playlist_id, user=request.user)
    all_songs = Song.objects.all()
    return render(request, 'playlist_detail.html', {'playlist': playlist, 'all_songs': all_songs})


@login_required
def add_song_to_playlist(request, playlist_id, song_id):
    playlist = Playlist.objects.get(id=playlist_id, user=request.user)
    song = Song.objects.get(id=song_id)
    playlist.songs.add(song)
    return redirect('playlist_detail', playlist_id=playlist.id)


@login_required
def remove_song_from_playlist(request, playlist_id, song_id):
    playlist = Playlist.objects.get(id=playlist_id, user=request.user)
    song = Song.objects.get(id=song_id)
    playlist.songs.remove(song)
    return redirect('playlist_detail', playlist_id=playlist.id)
@login_required
def play_song(request, song_id):
    song = Song.objects.get(id=song_id)
    song.play_count += 1
    song.save()
    ListeningHistory.objects.create(user=request.user, song=song)
    return JsonResponse({'status': 'ok', 'play_count': song.play_count})
@login_required
def analytics_dashboard(request):
    songs = Song.objects.all()
    top_songs = songs.order_by('-play_count')[:10]

    top_artists = (
        songs.values('artist')
        .annotate(total_plays=Sum('play_count'))
        .order_by('-total_plays')[:10]
    )

    total_songs = songs.count()
    total_plays = songs.aggregate(total=Sum('play_count'))['total'] or 0
    total_playlists = Playlist.objects.filter(user=request.user).count()
    mood_data = (
        songs.values('mood')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    context = {
        'top_songs': top_songs,
        'top_artists': top_artists,
        'total_songs': total_songs,
        'total_plays': total_plays,
        'total_playlists': total_playlists,
        'mood_data': mood_data,
    }
    return render(request, 'analytics.html', context)
@login_required
def export_analytics_csv(request):
    songs = Song.objects.all().order_by('-play_count')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="lyrical_analytics.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Artist', 'Play Count'])

    for song in songs:
        writer.writerow([song.title, song.artist, song.play_count])

    return response
@login_required
def library_view(request):
    liked_songs = LikedSong.objects.filter(user=request.user).select_related('song')
    playlists = Playlist.objects.filter(user=request.user)
    return render(request, 'library.html', {
        'liked_songs': liked_songs,
        'playlists': playlists,
    })


@login_required
def toggle_like(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    liked, created = LikedSong.objects.get_or_create(user=request.user, song=song)
    if not created:
        liked.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))
@login_required
def history_view(request):
    history = ListeningHistory.objects.filter(user=request.user).select_related('song')[:50]
    return render(request, 'history.html', {'history': history})
@login_required
def lyrics_timer(request):
    songs = Song.objects.all()
    return render(request, 'lyrics_timer.html', {'songs': songs})