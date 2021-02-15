from io import BytesIO
import tekore as tk
import requests
import plotly.graph_objects as go
from plotly.offline import plot
import networkx as nx
import matplotlib.image as mpimg
from urllib.request import urlopen
from PIL import Image
from skimage import io

client_id = 'dff21b856c2f4618a94b22a44c8c0a6f'
client_secret = '9995bff098c64c85bb99477c89a8a468'
token = tk.request_client_token(client_id, client_secret)
spotify = tk.Spotify(token)

# Too Door Cinema Club: 536BYVgOnRky0xjsPT96zl


def spotify_stuff():

    album = spotify.album('3RBULTZJ97bvVzZLpxcB0j')

    div = "<ul>"
    for track in album.tracks.items:
        div += "<li>{}, {}</li>".format(track.track_number, track.name)
        # print(track.track_number, track.name)
    div += "<li>{}</li>".format(get_image("536BYVgOnRky0xjsPT96zl"))
    div += "</ul>"
    return div


def get_image(artist):
    img_url = spotify.artist(artist).images[0].url
    # f = urlopen(img_url)
    # img_bytes = io.BytesIO(urlopen(img_url).read())
    # img = Image.open(img_url)
    # img = io.imread(img_url)
    return Image.open(BytesIO(requests.get(img_url).content))



