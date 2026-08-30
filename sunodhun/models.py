from django.db import models
from django.contrib.auth.models import User


class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to='album_covers/', blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.artist}"


class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs', blank=True, null=True)
    audio_file = models.FileField(upload_to='songs/')
    duration = models.PositiveIntegerField(help_text="Duration in seconds", blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    play_count = models.PositiveIntegerField(default=0)
    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('energetic', 'Energetic'),
        ('calm', 'Calm'),
        ('romantic', 'Romantic'),
    ]
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, blank=True, null=True, editable=False)

    LANGUAGE_CHOICES = [
        ('bollywood', 'Bollywood'),
        ('punjabi', 'Punjabi'),
        ('other', 'Other'),
    ]
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='other')
    lyrics = models.TextField(blank=True, null=True, help_text="LRC format: [00:12.00]Line text")
    def __str__(self):
        return f"{self.title} by {self.artist}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.mood and self.audio_file:
            try:
                from .mood_detector import detect_mood
                self.mood = detect_mood(self.audio_file.path)
                super().save(update_fields=['mood'])
            except Exception as e:
                import traceback
                print("Mood detect nahi ho paya:")
                print(''.join(traceback.format_exception(type(e), e, e.__traceback__)))


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    name = models.CharField(max_length=200)
    songs = models.ManyToManyField(Song, related_name='playlists', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class LikedSong(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_songs')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='liked_by')
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'song')

    def __str__(self):
        return f"{self.user.username} liked {self.song.title}"


class ListeningHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    played_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-played_at']

    def __str__(self):
        return f"{self.user.username} played {self.song.title}"