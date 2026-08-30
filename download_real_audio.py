import os
import requests
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lyrical.settings')
django.setup()

from sunodhun.models import Song, Album

media_songs_dir = os.path.join(os.path.dirname(__file__), 'media', 'songs')
os.makedirs(media_songs_dir, exist_ok=True)

TRACKS_TO_FETCH = [
    {
        "search": "Pasoori Ali Sethi",
        "title": "Pasoori",
        "artist": "Ali Sethi x Shae Gill",
        "album": "Coke Studio Season 14",
        "language": "punjabi",
        "mood": "energetic",
        "filename": "pasoori_official.m4a",
        "lyrics": """[00:00.00]Poochhe na koi mainu, ki ho gaya ae tere naal...
[00:04.00]Jaawaan main kahan? Dhoondhe tainu dil mera...
[00:08.00]Raataan langiyaan, taariyaan naal gal baataan kar ke!
[00:13.00]Aag laawaan main is doori nu, jehri saanu juda kare!
[00:18.00]Tere bina jeena ban gaya ae ik saza...
[00:22.00]Rowaan main kalla, sune na koi meri sada...
[00:26.00]Poochhe na koi mainu, ki ho gaya ae tere naal..."""
    },
    {
        "search": "Kesariya Arijit Singh",
        "title": "Kesariya",
        "artist": "Arijit Singh",
        "album": "Brahmastra",
        "language": "bollywood",
        "mood": "romantic",
        "filename": "kesariya_official.m4a",
        "lyrics": """[00:00.00]Mujhko sabhi se chheen le tum...
[00:05.00]Kesariya tera ishq hai piya...
[00:10.00]Rang jaaun jo main haath lagaun...
[00:15.00]Din beete saara teri khidmat mein...
[00:20.00]Kesariya tera ishq hai piya..."""
    },
    {
        "search": "Kahani Suno Kaifi Khalil",
        "title": "Kahani Suno 2.0",
        "artist": "Kaifi Khalil",
        "album": "Kahani Suno Single",
        "language": "other",
        "mood": "romantic",
        "filename": "kahani_suno_official.m4a",
        "lyrics": """[00:00.00]Kahani suno, zubaani suno...
[00:05.00]Mujhe pyaar hua tha, iqraar hua tha...
[00:10.00]Deewana hua, mastaana hua...
[00:15.00]Teri chaahat mein yeh dil naadaan hua...
[00:20.00]Kahani suno, zubaani suno..."""
    },
    {
        "search": "Tajdar e Haram Atif Aslam",
        "title": "Tajdar-e-Haram",
        "artist": "Atif Aslam",
        "album": "Coke Studio Season 8",
        "language": "other",
        "mood": "calm",
        "filename": "tajdar_e_haram_official.m4a",
        "lyrics": """[00:00.00]Kasamparsi pe meri nigah-e-karam...
[00:06.00]Tujh se fariyaad karte hain hum ae Shahenshah-e-Haram!
[00:12.00]Nigah-e-karam, nigah-e-karam...
[00:18.00]Ya Mustafa, Ya Mujtaba...
[00:24.00]Tajdar-e-Haram, ho karam..."""
    },
    {
        "search": "Mi Amor Sharn",
        "title": "Mi Amor",
        "artist": "Sharn, The Paul x 408",
        "album": "Mi Amor EP",
        "language": "punjabi",
        "mood": "happy",
        "filename": "mi_amor_official.m4a",
        "lyrics": """[00:00.00]Tere naal ho gaya pyaar mainu sachi...
[00:05.00]Akhiyaan 'ch akhiyaan paawen zara...
[00:10.00]Mera dil, mera saah tere naam keeta...
[00:15.00]Mi Amor, tu hi mera pyaar..."""
    },
    {
        "search": "Tu Jhoom Abida Parveen",
        "title": "Tu Jhoom",
        "artist": "Abida Parveen x Naseebo Lal",
        "album": "Coke Studio Season 14",
        "language": "punjabi",
        "mood": "calm",
        "filename": "tu_jhoom_official.m4a",
        "lyrics": """[00:00.00]Main raazi aan, main raazi aan...
[00:06.00]Tu jhoom, tu jhoom...
[00:12.00]Jo vi miliya ae rab koloon sohna miliya...
[00:18.00]Tu jhoom, tu jhoom..."""
    },
    {
        "search": "Lover Diljit Dosanjh",
        "title": "Lover",
        "artist": "Diljit Dosanjh",
        "album": "MoonChild Era",
        "language": "punjabi",
        "mood": "energetic",
        "filename": "lover_official.m4a",
        "lyrics": """[00:00.00]Tera ni main, tera ni main lover...
[00:05.00]Ho gaya ni kudiye sohniye tera lover...
[00:10.00]Dil tera mangda ik baar, lover!
[00:15.00]Ni main tera lover!"""
    },
    {
        "search": "Tum Hi Ho Arijit Singh",
        "title": "Tum Hi Ho",
        "artist": "Arijit Singh",
        "album": "Aashiqui 2",
        "language": "bollywood",
        "mood": "romantic",
        "filename": "tum_hi_ho_official.m4a",
        "lyrics": """[00:00.00]Hum tere bin ab reh nahi sakte...
[00:05.00]Tere bina kya wajood mera...
[00:10.00]Kyunki tum hi ho, ab tum hi ho...
[00:15.00]Zindagi ab tum hi ho...
[00:20.00]Chain bhi, mera dard bhi...
[00:25.00]Meri aashiqui ab tum hi ho..."""
    },
    {
        "search": "Apna Bana Le Arijit Singh",
        "title": "Apna Bana Le",
        "artist": "Arijit Singh",
        "album": "Bhediya",
        "language": "bollywood",
        "mood": "romantic",
        "filename": "apna_bana_le_official.m4a",
        "lyrics": """[00:00.00]Tu mera koi na hoke bhi kuch lage...
[00:05.00]Apna bana le mujhe, apna bana le...
[00:10.00]Dil ke nagar mein shehar bana le...
[00:15.00]Apna bana le mujhe piya..."""
    },
    {
        "search": "Raataan Lambiyan Jubin Nautiyal",
        "title": "Raataan Lambiyan",
        "artist": "Jubin Nautiyal & Asees Kaur",
        "album": "Shershaah",
        "language": "bollywood",
        "mood": "romantic",
        "filename": "raataan_lambiyan_official.m4a",
        "lyrics": """[00:00.00]Teri meri gallan ho gayi mashhoor...
[00:05.00]Kar na kabhi tu mujhe nazron se door...
[00:10.00]Kithe chaliye tu kithe chaliye...
[00:15.00]Raataan lambiyan lambiyan re..."""
    }
]

print("Starting iTunes official audio lookup and download...")

for item in TRACKS_TO_FETCH:
    try:
        url = f"https://itunes.apple.com/search?term={requests.utils.quote(item['search'])}&entity=song&limit=1"
        res = requests.get(url, timeout=10).json()
        
        if res.get('results'):
            track_info = res['results'][0]
            preview_url = track_info['previewUrl']
            
            audio_dest = os.path.join(media_songs_dir, item['filename'])
            print(f"Downloading official audio for '{item['title']}' from iTunes...")
            
            audio_bytes = requests.get(preview_url, timeout=15).content
            with open(audio_dest, 'wb') as f:
                f.write(audio_bytes)
                
            album_obj, _ = Album.objects.get_or_create(
                title=item['album'],
                defaults={'artist': item['artist']}
            )
            
            relative_path = f"songs/{item['filename']}"
            
            song_obj, created = Song.objects.get_or_create(
                title=item['title'],
                defaults={
                    'artist': item['artist'],
                    'album': album_obj,
                    'audio_file': relative_path,
                    'duration': 30,
                    'language': item['language'],
                    'mood': item['mood'],
                    'lyrics': item['lyrics'],
                    'play_count': 42
                }
            )
            
            song_obj.artist = item['artist']
            song_obj.album = album_obj
            song_obj.audio_file = relative_path
            song_obj.duration = 30
            song_obj.language = item['language']
            song_obj.mood = item['mood']
            song_obj.lyrics = item['lyrics']
            song_obj.save()
            
            print(f"Downloaded and updated '{item['title']}' by {item['artist']} with real official audio!")
        else:
            print(f"No result found for '{item['search']}'")
    except Exception as e:
        print(f"Error fetching {item['title']}: {e}")

print("\nDone downloading and updating database with real audio files!")
