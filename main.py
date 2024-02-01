from get_response import storeGPT
from get_values import getValues
from get_song import find_recommendations
import json

# Load data from the JSON file


def findSong(name):
    storeGPT(name)
    getValues()
    with open('values.json', 'r') as json_file:
        data = json.load(json_file)
    songs = []
    for track in find_recommendations(data['Danceability'], data['Energy'], data['Instrumentalness'], data['Liveness'], data['Loudness'], data['Tempo'], data['Valence'])['tracks']:
        songs.append(track['external_urls']['spotify'])
    
    return songs

# print (findSong('images/swang.jpg'))
