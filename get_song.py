import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import numpy as np

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(client_id="3df409a8be3441319607bd8745d34c31",
                                                        client_secret="4ae9fa9feefe46568eb2d39dec9a4a8f"))


def generate_biased_random_number():
    # Define the mean and standard deviation for the normal distribution
    mean = 80  # Mean of 50 (middle of the range 0-100)
    std_dev = 15  # You can adjust this value to control the bias

    # Generate a random number from a normal distribution with the specified mean and std_dev
    random_number = int(np.random.normal(mean, std_dev))

    # Ensure the generated number is within the range [0, 100]
    random_number = max(0, min(100, random_number))

    return random_number

def find_recommendations(danceability, energy, instrumentalness, liveness, loudness, tempo, valence, seed_genres=['pop', 'rap', 'hardstyle', 'rock', 'lofi'], target_popularity=generate_biased_random_number(), limit=5):
    recommendations = spotify.recommendations(seed_genres=seed_genres,
                                              target_danceability=danceability,
                                              target_energy=energy,
                                              target_instrumentalness=instrumentalness,
                                              target_liveness=liveness,
                                              target_loudness=loudness,
                                              target_tempo=tempo,
                                              target_valence=valence,
                                              target_popularity=target_popularity,
                                              limit=limit)
    return recommendations
