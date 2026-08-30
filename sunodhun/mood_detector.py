# sunodhun/mood_detector.py

import librosa
import numpy as np

def detect_mood(audio_path):
    # Poora song load karne ki zaroorat nahi, pehle 30 second kaafi hain (speed ke liye)
    # sr=None isliye rakha hai taaki original sample rate pe hi load ho, resampling (soxr) na lage
    y, sr = librosa.load(audio_path, duration=30, sr=None)

    # Tempo = gaane ki speed (beats per minute)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # RMS energy = gaana kitna "loud/energetic" hai
    rms = np.mean(librosa.feature.rms(y=y))

    # Spectral centroid = sound kitna "bright/sharp" hai (high value = bright sound)
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))

    # Zero crossing rate = sound kitna noisy/rough hai (kam value = smooth/soft sound)
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=y))

    # Simple rule-based algorithm: in features ke combination se mood decide karte hain
    if tempo > 120 and rms > 0.05:
        mood = "energetic"
    elif tempo > 100 and spectral_centroid > 2500:
        mood = "happy"
    elif tempo < 80 and rms < 0.03:
        mood = "sad"
    elif zcr < 0.05 and rms < 0.04:
        mood = "calm"
    else:
        mood = "romantic"
    print(f"[DEBUG] tempo={tempo}, rms={rms:.4f}, spectral_centroid={spectral_centroid:.2f}, zcr={zcr:.4f}")
    return mood