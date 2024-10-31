import base64
from requests import post, get
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='keys.env')

spotify_credentials = {
    "client_id" : f"{os.getenv('spotify_client_id')}",
    "client_secret" : f"{os.getenv('spotify_client_secret')}",
    "redirect_uri" : "https://localhost:5000/callback", 
    "scope" : "playlist-read-private"
}

# get access token
def getToken():
    auth_string = spotify_credentials["client_id"] + ":" + spotify_credentials["client_secret"]
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization" : f"Basic {auth_base64}"
    }
    data = {"grant_type" : "client_credentials"}
    result = post(url=url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return(token)

# get header
def get_auth_header(token):
    return({"Authorization": f"Bearer {token}"})

# playlist getter
def get_playlist(token, p_id):
    playlist_id = p_id
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return(json_result)

# playlist id finder
def get_playlist_id(url):
    if '?' in url:
        x = url.split('?')
        x = x[0]
        x = url.split('/')
        x = x[-1]
        x = x.split('?')
        x = x[0]
        return(x)
    else:
        x = url.split('/')
        x = x[-1]
        x = x.split('?')
        x = x[0]
        return(x)

# called during POST request
def get_playlist_details(url):
    x = getToken()
    playlist_id = get_playlist_id(url=url)
    y = get_playlist(token=x, p_id=playlist_id)

    songs = []
    for song in (y['tracks'])['items']:
        songs.append((song['track'])['name'])

    # # getting artist names
    artists =[]
    for song in ((y['tracks'])['items']):
        temp_artists = []
        for artist in ((song["track"])['artists']):
            temp_artists.append(artist["name"])
        artists.append(temp_artists)

    return_list = []
    for j in range(len(artists)):
        return_list.append(f"{artists[j]}: {songs[j]}")

    return(return_list)
