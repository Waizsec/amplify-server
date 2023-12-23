from transformers import pipeline
from flask import request
import librosa
import numpy as np
import torchaudio
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

model_name = "dima806/music_genres_classification"

audio_classification = pipeline(
    task="audio-classification",
    model=model_name,
    framework="pt",
)


def audio_classify(audio_file_path):

    waveform, sample_rate = torchaudio.load(audio_file_path)
    if sample_rate != 44100:
        resampler = torchaudio.transforms.Resample(sample_rate, 44100)
        waveform = resampler(waveform)
    audio_np = waveform.numpy()[0]
    result = audio_classification(audio_np)
    genre = max(result, key=lambda x: x['score'])['label']

    y, sr = librosa.load(audio_file_path, sr=None)

    onset_env = librosa.onset.onset_strength(y=y, sr=sr)

    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

    loudness = np.mean(librosa.feature.rms(y=y))

    danceability = tempo / 180.0

    chromagram = librosa.feature.chroma_stft(y=y, sr=sr)
    mean_chroma = np.mean(chromagram, axis=1)
    chroma_to_key = ['C', 'C#', 'D', 'D#', 'E',
                     'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    estimated_key_index = np.argmax(mean_chroma)
    estimated_key = chroma_to_key[estimated_key_index]
    estimated_mode = "Major" if mean_chroma[estimated_key_index] > np.mean(
        mean_chroma) else "Minor"
    liveness = np.mean(librosa.feature.rms(y=y))

    result = {
        "Key": estimated_key,
        "Mode": estimated_mode,
        "Tempo": float(tempo),
        "Loudness": float(loudness),
        "Danceability": float(danceability),
        "Liveness": float(liveness),
        "KeyIndex": int(estimated_key_index),
        "genre": genre
    }

    # Convert NumPy arrays to Python lists
    result["Chromagram"] = ""
    result["Waveform"] = ""

    return result
