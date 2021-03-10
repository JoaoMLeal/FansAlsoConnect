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
    div += "<li>{}</li>".format(get_image("536BYVgOnRky0xjsPT96zl"))
    div += "</ul>"
    return div


def get_image(artist=too_door):
    return spotify.artist(artist).images[0].url
    #return Image.open(BytesIO(requests.get(img_url).content))




