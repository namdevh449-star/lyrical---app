import os
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lyrical.settings')
django.setup()

from sunodhun.models import Song, Album
from django.core.files import File

# Ensure media/songs directory exists
media_songs_dir = os.path.join(os.path.dirname(__file__), 'media', 'songs')
os.makedirs(media_songs_dir, exist_ok=True)

# Find an existing audio file as source template
template_audio = None
for fname in os.listdir(media_songs_dir):
    if fname.endswith(('.mp4', '.mp3', '.m4a')):
        template_audio = os.path.join(media_songs_dir, fname)
        break

if not template_audio:
    # Create a tiny dummy mp3 file if none exists
    template_audio = os.path.join(media_songs_dir, 'sample_audio.mp3')
    with open(template_audio, 'wb') as f:
        f.write(b'ID3\x03\x00\x00\x00\x00\x00\x00' + b'\x00' * 1000)

print(f"Using template audio: {template_audio}")

NEW_SONGS = [
    {
        "title": "Pasoori",
        "artist": "Ali Sethi x Shae Gill",
        "album": "Coke Studio Season 14",
        "language": "punjabi",
        "mood": "energetic",
        "duration": 224,
        "filename": "pasoori.mp3",
        "lyrics": """[00:00.00]Poochhe na koi mainu, ki ho gaya ae tere naal...
[00:05.00]Jaawaan main kahan? Dhoondhe tainu dil mera...
[00:10.00]Raataan langiyaan, taariyaan naal gal baataan kar ke!
[00:15.00]Aag laawaan main is doori nu, jehri saanu juda kare!
[00:20.00]Tere bina jeena ban gaya ae ik saza...
[00:25.00]Rowaan main kalla, sune na koi meri sada...
[00:30.00]Poochhe na koi mainu, ki ho gaya ae tere naal..."""
    },
    {
        "title": "Kesariya",
        "artist": "Arijit Singh",
        "album": "Brahmastra",
        "language": "bollywood",
        "mood": "romantic",
        "duration": 268,
        "filename": "kesariya.mp3",
        "lyrics": """[00:00.00]Mujhko sabhi se chheen le tum...
[00:06.00]Kesariya tera ishq hai piya...
[00:12.00]Rang jaaun jo main haath lagaun...
[00:18.00]Din beete saara teri khidmat mein..."""
    },
    {
        "title": "Kahani Suno 2.0",
        "artist": "Kaifi Khalil",
        "album": "Kahani Suno Single",
        "language": "other",
        "mood": "romantic",
        "duration": 172,
        "filename": "kahani_suno.mp3",
        "lyrics": """[00:00.00]Kahani suno, zubaani suno...
[00:05.00]Mujhe pyaar hua tha, iqraar hua tha...
[00:10.00]Deewana hua, mastaana hua...
[00:15.00]Teri chaahat mein yeh dil naadaan hua..."""
    },
    {
        "title": "Tajdar-e-Haram",
        "artist": "Atif Aslam",
        "album": "Coke Studio Season 8",
        "language": "other",
        "mood": "calm",
        "duration": 380,
        "filename": "tajdar_e_haram.mp3",
        "lyrics": """[00:00.00]Kasamparsi pe meri nigah-e-karam...
[00:07.00]Tujh se fariyaad karte hain hum ae Shahenshah-e-Haram!
[00:15.00]Nigah-e-karam, nigah-e-karam..."""
    },
    {
        "title": "Mi Amor",
        "artist": "Sharn, The Paul x 408",
        "album": "Mi Amor EP",
        "language": "punjabi",
        "mood": "happy",
        "duration": 195,
        "filename": "mi_amor.mp3",
        "lyrics": """[00:00.00]Tere naal ho gaya pyaar mainu sachi...
[00:06.00]Akhiyaan 'ch akhiyaan paawen zara...
[00:12.00]Mera dil, mera saah tere naam keeta..."""
    },
    {
        "title": "Tu Jhoom",
        "artist": "Abida Parveen x Naseebo Lal",
        "album": "Coke Studio Season 14",
        "language": "punjabi",
        "mood": "calm",
        "duration": 310,
        "filename": "tu_jhoom.mp3",
        "lyrics": """[00:00.00]Main raazi aan, main raazi aan...
[00:06.00]Tu jhoom, tu jhoom...
[00:12.00]Jo vi miliya ae rab koloon sohna miliya..."""
    },
    {
        "title": "Lover",
        "artist": "Diljit Dosanjh",
        "album": "MoonChild Era",
        "language": "punjabi",
        "mood": "energetic",
        "duration": 210,
        "filename": "lover.mp3",
        "lyrics": """[00:00.00]Tera ni main, tera ni main lover...
[00:05.00]Ho gaya ni kudiye sohniye tera lover...
[00:10.00]Dil tera mangda ik baar, lover!"""
    },
    {
        "title": "Tum Hi Ho",
        "artist": "Arijit Singh",
        "album": "Aashiqui 2",
        "language": "bollywood",
        "mood": "romantic",
        "duration": 262,
        "filename": "tum_hi_ho.mp3",
        "lyrics": """[00:00.00]Hum tere bin ab reh nahi sakte...
[00:06.00]Tere bina kya wajood mera...
[00:12.00]Kyunki tum hi ho, ab tum hi ho...
[00:18.00]Zindagi ab tum hi ho..."""
    }
]

created_count = 0
for song_data in NEW_SONGS:
    album_obj, _ = Album.objects.get_or_create(
        title=song_data["album"],
        defaults={"artist": song_data["artist"]}
    )

    dest_audio_path = os.path.join(media_songs_dir, song_data["filename"])
    if not os.path.exists(dest_audio_path):
        shutil.copy(template_audio, dest_audio_path)

    relative_audio_path = f"songs/{song_data['filename']}"

    song_obj, created = Song.objects.get_or_create(
        title=song_data["title"],
        artist=song_data["artist"],
        defaults={
            "album": album_obj,
            "audio_file": relative_audio_path,
            "duration": song_data["duration"],
            "language": song_data["language"],
            "mood": song_data["mood"],
            "lyrics": song_data["lyrics"],
            "play_count": 15
        }
    )

    if not created:
        song_obj.album = album_obj
        song_obj.audio_file = relative_audio_path
        song_obj.duration = song_data["duration"]
        song_obj.language = song_data["language"]
        song_obj.mood = song_data["mood"]
        song_obj.lyrics = song_data["lyrics"]
        song_obj.save()

    created_count += 1
    print(f"Added/Updated Song: '{song_obj.title}' by {song_obj.artist}")

print(f"\nSuccessfully added {created_count} new songs with artists & synced lyrics to database!")

