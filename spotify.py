import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def get_spotify_recommendations(seed_genre, seed_tempo, seed_loudness, seed_danceability, seed_keyindex, seed_liveness):
    if seed_genre == "null" or seed_tempo == "null" or seed_loudness == "null" or seed_danceability == "null" or seed_keyindex == "null" or seed_liveness == "null":
        recommendations = ['']
    else:
        recommendations = [seed_genre, seed_tempo, seed_loudness,
                           seed_danceability, seed_keyindex, seed_liveness]
        client_id = '9fbdd42f71f44b19b7aa4098a14348b5'
        client_secret = '384d1669aec94830bf93f7d462ab673f'

        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret))

        recommendations = sp.recommendations(
            seed_genres=[seed_genre],
            target_tempo=seed_tempo,
            target_loudness=seed_loudness,
            target_danceability=seed_danceability,
            target_key=seed_keyindex,
            target_liveness=seed_liveness,
            limit=10
        )

    return recommendations
