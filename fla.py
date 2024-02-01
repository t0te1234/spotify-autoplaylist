from flask_cors import CORS
from datetime import datetime
from datetime import date
import requests
from flask import *
from flask import Flask, request, render_template, redirect, url_for
from fileinput import filename 
import os
from werkzeug.utils import secure_filename
from main import findSong
import random


app = Flask(__name__)
CORS(app)
app.secret_key = 'dasdio12909kpok'

client_id = '64f1524ada334d40a89ddf08b6a67a00'
client_secret = '173ebf295352482490a7c037214b6171'
redirect_uri = 'http://localhost:5000/callback'

SPOTIFY_CLIENT_ID = '64f1524ada334d40a89ddf08b6a67a00'
SPOTIFY_CLIENT_SECRET = '173ebf295352482490a7c037214b6171'
SPOTIFY_REDIRECT_URI = 'http://localhost:5000/callback'
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1/'
app.config['UPLOAD_FOLDER'] = 'static/images/'
global is_member
is_member = True


auth_url = "https://accounts.spotify.com/api/authorize"
token_url = "https://accounts.spotify.com/api/token"
api_base_url = "https://api.spotify.com/v1/"


@app.route('/')
def index():
    return "Welcome <a href='/login'>Login</a> & <a href='/memberin'>Login-member</a> & <a href='/upload'>Upload File</a>"

@app.route('/login')
def login():
    global is_member 
    is_member = False
    scope = 'user-read-private user-read-email playlist-modify-private'  # Add any additional scopes you need
    auth_url = f"{SPOTIFY_AUTH_URL}?client_id={SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={SPOTIFY_REDIRECT_URI}&scope={scope}"
    return redirect(auth_url)

@app.route('/memberin')
def memerin():
    global is_member
    is_member = True
    scope = 'user-read-private user-read-email playlist-modify-private'  # Add any additional scopes you need
    auth_url = f"{SPOTIFY_AUTH_URL}?client_id={SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={SPOTIFY_REDIRECT_URI}&scope={scope}"
    return redirect(auth_url)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            filename = secure_filename(file.filename)
            extension = os.path.splitext(filename)[1]
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image' + extension)
            file.save(save_path)
            # Note that 'static' should not be included in the filename argument here
            image_url = url_for('static', filename=f'images/image{extension}')
            return jsonify({'imagePath': image_url})
    return redirect(url_for('index'))


@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})

    if 'code' not in request.args:
        return jsonify({"error": "Authorization code not found in the request"})

    req_body = {
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(token_url, data=req_body)
    token_info = response.json()

    session['access_token'] = token_info.get('access_token')
    session['refresh_token'] = token_info.get('refresh_token')
    session['expires_at'] = datetime.now().timestamp() + token_info.get('expires_in', 0)
    
    if is_member:
        return redirect(url_for('make_moment_playlist'))
    else:
        return redirect(url_for('make_playlists'))

@app.route('/playlists')
def make_playlists():
    # Check if the access token is available and valid
    if 'access_token' not in session or 'expires_at' not in session or session['expires_at'] < datetime.now().timestamp():
        return redirect('/login')  # or handle token refresh

    # Read song URLs from the .txt file
    with open('songs.txt', 'r') as file:
        song_urls = file.readlines()

    # Extract track IDs from URLs
    track_ids = [url.split('/')[-1].strip() for url in song_urls]

    # Empty the songs.txt file
    with open('songs.txt', 'w') as file:
        file.truncate(0)

    # Create a new playlist
    headers = {
        'Authorization': f"Bearer {session['access_token']}",
        'Content-Type': 'application/json'
    }
    user_info = requests.get(f"{api_base_url}me", headers=headers).json()
    user_id = user_info['id']
    
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    name = 'Your Day Wrapped: ' + d1
    
    playlist_data = {
        'name': name,
        'description': 'This is what you heard today',
        'public': False  # Set to True if you want the playlist to be public
    }
    create_response = requests.post(f"{api_base_url}users/{user_id}/playlists", headers=headers, json=playlist_data)
    playlist_id = create_response.json()['id']

    # Add tracks to the playlist
    add_tracks_data = {'uris': [f'spotify:track:{track_id}' for track_id in track_ids]}
    requests.post(f"{api_base_url}playlists/{playlist_id}/tracks", headers=headers, json=add_tracks_data)

    # Redirect or send a success response
    return redirect('/success')  # Replace with your success page

    
@app.route('/refresh-token')
def refresh_token():
    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id' : client_id,
            'client_secret': client_secret
        }
    response = request.post(token_url, data=req_body)
    new_token_info = response.json()
    
    session['access_token'] = new_token_info['access_token']
    session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']
    return redirect('/login')

@app.route('/success')
def end():
    return "Welcome <a href='/login'>Login</a> & <a href='/memberin'>Login-member</a> & <a href='/upload'>Upload File</a>"

@app.route('/playlists-members')
def make_moment_playlist():
    # Check if the access token is available and valid
    if 'access_token' not in session or 'expires_at' not in session or session['expires_at'] < datetime.now().timestamp():
        return redirect('/login')  # or handle token refresh
    
    if (os.listdir('static/images')[0] == "image.jpg"):
        song_urls = findSong("static/images/image.jpg")
    elif (os.listdir('static/images')[0] == "image.jpeg"):
        song_urls = findSong("static/images/image.jpeg")
    else:
        song_urls = findSong("static/images/image.png")

    # Extract track IDs from URLs
    track_ids = [url.split('/')[-1].strip() for url in song_urls]

    # Create a new playlist
    headers = {
        'Authorization': f"Bearer {session['access_token']}",
        'Content-Type': 'application/json'
    }
    user_info = requests.get(f"{api_base_url}me", headers=headers).json()
    user_id = user_info['id']

    playlist_data = {
        'name': 'Your Moment.....',
        'description': 'Heres some music for what you are doing right now',
        'public': False  # Set to True if you want the playlist to be public
    }
    create_response = requests.post(f"{api_base_url}users/{user_id}/playlists", headers=headers, json=playlist_data)
    playlist_id = create_response.json()['id']
    
    selected_songs = random.sample(song_urls, 2)
    with open("songs.txt", "a") as file:
        for song in selected_songs:
            file.write(song + "\n")
    
    # Add tracks to the playlist
    add_tracks_data = {'uris': [f'spotify:track:{track_id}' for track_id in track_ids]}
    requests.post(f"{api_base_url}playlists/{playlist_id}/tracks", headers=headers, json=add_tracks_data)
    
    playlist_link = f"https://open.spotify.com/playlist/{playlist_id}"
    
    # Redirect or send a success response
    return jsonify({'playlistId': playlist_link})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)