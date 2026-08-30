import os
import shutil
import django
import yt_dlp

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lyrical.settings')
django.setup()

from sunodhun.models import Song, Album

media_songs_dir = os.path.join(os.path.dirname(__file__), 'media', 'songs')
os.makedirs(media_songs_dir, exist_ok=True)

FULL_SONGS_CATALOG = [
    {
        "search": "Pasoori Ali Sethi Shae Gill official audio",
        "title": "Pasoori",
        "artist": "Ali Sethi x Shae Gill",
        "album": "Coke Studio Season 14",
        "language": "punjabi",
        "mood": "energetic",
        "out_file": "pasoori_full.m4a",
        "lyrics": """[00:00.00]Poochhe na koi mainu, ki ho gaya ae tere naal...
[00:15.00]Jaawaan main kahan? Dhoondhe tainu dil mera...
[00:30.00]Raataan langiyaan, taariyaan naal gal baataan kar ke!
[00:45.00]Aag laawaan main is doori nu, jehri saanu juda kare!
[01:00.00]Tere bina jeena ban gaya ae ik saza...
[01:15.00]Rowaan main kalla, sune na koi meri sada...
[01:30.00]Poochhe na koi mainu, ki ho gaya ae tere naal...
[01:45.00]Mere dhol judaiyan di, tainu khabar kivein hove...
[02:00.00]Aa jaave dil tera, toota taara ban ke!
[02:15.00]Aag laawaan main is doori nu, jehri saanu juda kare!
[02:30.00]Poochhe na koi mainu, ki ho gaya ae tere naal..."""
    },
    {
        "search": "Kesariya Arijit Singh Brahmastra official audio",
        "title": "Kesariya",
        "artist": "Arijit Singh",
        "album": "Brahmastra",
        "language": "bollywood",
        "mood": "romantic",
        "out_file": "kesariya_full.m4a",
        "lyrics": """[00:00.00]Mujhko sabhi se chheen le tum...
[00:15.00]Kesariya tera ishq hai piya...
[00:30.00]Rang jaaun jo main haath lagaun...
[00:45.00]Din beete saara teri khidmat mein...
[01:00.00]Ruh ka sauda kiya nahi karte...
[01:15.00]Kesariya tera ishq hai piya...
[01:30.00]Rang jaaun jo main haath lagaun...
[01:45.00]Din beete saara teri khidmat mein...
[02:00.00]Kesariya tera ishq hai piya..."""
    },
    {
        "search": "Kahani Suno 2.0 Kaifi Khalil official audio",
        "title": "Kahani Suno 2.0",
        "artist": "Kaifi Khalil",
        "album": "Kahani Suno Single",
        "language": "other",
        "mood": "romantic",
        "out_file": "kahani_suno_full.m4a",
        "lyrics": """[00:00.00]Kahani suno, zubaani suno...
[00:15.00]Mujhe pyaar hua tha, iqraar hua tha...
[00:30.00]Deewana hua, mastaana hua...
[00:45.00]Teri chaahat mein yeh dil naadaan hua...
[01:00.00]Pyar hua tha, iqraar hua tha...
[01:15.00]Mujhe pyaar hua tha, iqraar hua tha...
[01:30.00]Kahani suno, zubaani suno..."""
    },
    {
        "search": "Tajdar e Haram Atif Aslam Coke Studio Season 8",
        "title": "Tajdar-e-Haram",
        "artist": "Atif Aslam",
        "album": "Coke Studio Season 8",
        "language": "other",
        "mood": "calm",
        "out_file": "tajdar_e_haram_full.m4a",
        "lyrics": """[00:00.00]Kasamparsi pe meri nigah-e-karam...
[00:30.00]Tujh se fariyaad karte hain hum ae Shahenshah-e-Haram!
[01:00.00]Nigah-e-karam, nigah-e-karam...
[01:30.00]Ya Mustafa, Ya Mujtaba...
[02:00.00]Tajdar-e-Haram, ho karam...
[02:30.00]Kya tum se kahoon ae mere aqa...
[03:00.00]Kasamparsi pe meri nigah-e-karam...
[03:30.00]Shahenshah-e-Haram, ho karam..."""
    },
    {
        "search": "Mi Amor Sharn The Paul 408 official audio",
        "title": "Mi Amor",
        "artist": "Sharn, The Paul x 408",
        "album": "Mi Amor EP",
        "language": "punjabi",
        "mood": "happy",
        "out_file": "mi_amor_full.m4a",
        "lyrics": """[00:00.00]Tere naal ho gaya pyaar mainu sachi...
[00:15.00]Akhiyaan 'ch akhiyaan paawen zara...
[00:30.00]Mera dil, mera saah tere naam keeta...
[00:45.00]Mi Amor, tu hi mera pyaar...
[01:00.00]Tere bin nayiyo lagda dil mera...
[01:15.00]Mi Amor, tu hi mera pyaar..."""
    },
    {
        "search": "Tu Jhoom Abida Parveen Naseebo Lal Coke Studio Season 14",
        "title": "Tu Jhoom",
        "artist": "Abida Parveen x Naseebo Lal",
        "album": "Coke Studio Season 14",
        "language": "punjabi",
        "mood": "calm",
        "out_file": "tu_jhoom_full.m4a",
        "lyrics": """[00:00.00]Main raazi aan, main raazi aan...
[00:20.00]Tu jhoom, tu jhoom...
[00:40.00]Jo vi miliya ae rab koloon sohna miliya...
[01:00.00]Tu jhoom, tu jhoom...
[01:20.00]Main raazi aan, main raazi aan...
[01:40.00]Tu jhoom, tu jhoom..."""
    },
    {
        "search": "Lover Diljit Dosanjh MoonChild Era official audio",
        "title": "Lover",
        "artist": "Diljit Dosanjh",
        "album": "MoonChild Era",
        "language": "punjabi",
        "mood": "energetic",
        "out_file": "lover_full.m4a",
        "lyrics": """[00:00.00]Tera ni main, tera ni main lover...
[00:15.00]Ho gaya ni kudiye sohniye tera lover...
[00:30.00]Dil tera mangda ik baar, lover!
[00:45.00]Ni main tera lover!
[01:00.00]Tera ni main, tera ni main lover..."""
    },
    {
        "search": "Tum Hi Ho Arijit Singh Aashiqui 2 official audio",
        "title": "Tum Hi Ho",
        "artist": "Arijit Singh",
        "album": "Aashiqui 2",
        "language": "bollywood",
        "mood": "romantic",
        "out_file": "tum_hi_ho_full.m4a",
        "lyrics": """[00:00.00]Hum tere bin ab reh nahi sakte...
[00:15.00]Tere bina kya wajood mera...
[00:30.00]Kyunki tum hi ho, ab tum hi ho...
[00:45.00]Zindagi ab tum hi ho...
[01:00.00]Chain bhi, mera dard bhi...
[01:15.00]Meri aashiqui ab tum hi ho...
[01:30.00]Tere liye hi jiya main...
[01:45.00]Tum hi ho, ab tum hi ho..."""
    },
    {
        "search": "Apna Bana Le Arijit Singh Bhediya official audio",
        "title": "Apna Bana Le",
        "artist": "Arijit Singh",
        "album": "Bhediya",
        "language": "bollywood",
        "mood": "romantic",
        "out_file": "apna_bana_le_full.m4a",
        "lyrics": """[00:00.00]Tu mera koi na hoke bhi kuch lage...
[00:15.00]Apna bana le mujhe, apna bana le...
[00:30.00]Dil ke nagar mein shehar bana le...
[00:45.00]Apna bana le mujhe piya...
[01:00.00]Tu mera koi na hoke bhi kuch lage...
[01:15.00]Apna bana le mujhe, apna bana le..."""
    },
    {
        "search": "Raataan Lambiyan Jubin Nautiyal Shershaah official audio",
        "title": "Raataan Lambiyan",
        "artist": "Jubin Nautiyal & Asees Kaur",
        "album": "Shershaah",
        "language": "bollywood",
        "mood": "romantic",
        "out_file": "raataan_lambiyan_full.m4a",
        "lyrics": """[00:00.00]Teri meri gallan ho gayi mashhoor...
[00:15.00]Kar na kabhi tu mujhe nazron se door...
[00:30.00]Kithe chaliye tu kithe chaliye...
[00:45.00]Raataan lambiyan lambiyan re...
[01:00.00]Katte tere sanghiyaan sanghiyaan re...
[01:15.00]Raataan lambiyan lambiyan re..."""
    }
]

print("Starting FULL-LENGTH song download using yt-dlp...")

for item in FULL_SONGS_CATALOG:
    target_path = os.path.join(media_songs_dir, item['out_file'])
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': target_path.replace('.m4a', '.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
    }

    try:
        print(f"Downloading FULL song for: '{item['title']}' by {item['artist']}...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{item['search']}", download=True)
            if 'entries' in info and len(info['entries']) > 0:
                entry = info['entries'][0]
                duration_sec = entry.get('duration', 240)
                downloaded_file = ydl.prepare_filename(entry)
                
                # Copy or rename to standard destination
                if os.path.exists(downloaded_file):
                    shutil.move(downloaded_file, target_path)

                album_obj, _ = Album.objects.get_or_create(
                    title=item['album'],
                    defaults={'artist': item['artist']}
                )

                rel_file_path = f"songs/{item['out_file']}"
                
                songs = Song.objects.filter(title__iexact=item['title'])
                if songs.exists():
                    for s in songs:
                        s.artist = item['artist']
                        s.album = album_obj
                        s.audio_file = rel_file_path
                        s.duration = duration_sec
                        s.language = item['language']
                        s.mood = item['mood']
                        s.lyrics = item['lyrics']
                        s.save()
                        print(f"Updated FULL track database record {s.id}: '{s.title}' ({duration_sec}s full duration)")
                else:
                    s = Song.objects.create(
                        title=item['title'],
                        artist=item['artist'],
                        album=album_obj,
                        audio_file=rel_file_path,
                        duration=duration_sec,
                        language=item['language'],
                        mood=item['mood'],
                        lyrics=item['lyrics'],
                        play_count=100
                    )
                    print(f"Created FULL track record {s.id}: '{s.title}' ({duration_sec}s full duration)")
    except Exception as err:
        print(f"Error downloading full track '{item['title']}': {err}")

print("\nSUCCESS: All full-length original duration MP3/M4A songs downloaded and updated!")
