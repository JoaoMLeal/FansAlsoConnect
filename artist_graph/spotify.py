from io import BytesIO
import json
import tekore as tk
import requests
from PIL import Image

with open("D:\Projects\FansAlsoConnect\\artist_graph\\token.json") as f:
    data = json.load(f)

client_id = data['client_id']
client_secret = data['client_secret']
token = tk.request_client_token(client_id=client_id, client_secret=client_secret)
spotify = tk.Spotify(token)

too_door = "536BYVgOnRky0xjsPT96zl"


# Too Door Cinema Club: 536BYVgOnRky0xjsPT96zl


def spotify_stuff():
    album = spotify.album('3RBULTZJ97bvVzZLpxcB0j')

    div = "<ul>"
    for track in album.tracks.items:
        div += "<li>{}, {}</li>".format(track.track_number, track.name)
    div += "<li>{}</li>".format(get_artist_image_url("536BYVgOnRky0xjsPT96zl"))
    div += "</ul>"
    return div


def get_artist_image_url(artist=too_door):
    url = spotify.artist(artist).images[0].url
    return url


def get_related_artists_id(artist=too_door):
    artists = spotify.artist_related_artists(artist)
    artist_array = [a.id for a in artists]
    return artist_array


def get_related_artists_image(artist=too_door):
    return None
