import os
from io import BytesIO
import json
import tekore as tk
import requests
from PIL import Image

from fansalsoconnect.apps.artistgraph.model.artist import Artist

with open(os.getcwd() + "\\token.json") as f:
    data = json.load(f)

client_id = data['client_id']
client_secret = data['client_secret']
token = tk.request_client_token(client_id=client_id, client_secret=client_secret)
spotify = tk.Spotify(token)
too_door = "536BYVgOnRky0xjsPT96zl"
coldplay = "4gzpq5DPGxSnKTe4SA8HAU"


def get_artist_image_url(artist=coldplay):
    url = spotify.artist(artist).images[0].url
    return url


def get_related_artists_id(artist=coldplay):
    artists = spotify.artist_related_artists(artist)
    artist_array = [a.id for a in artists]
    return artist_array


def get_related_artists_image(artist=too_door):
    return None
