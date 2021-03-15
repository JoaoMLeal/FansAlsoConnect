import os
from io import BytesIO
import json
import tekore as tk
import requests
from PIL import Image

from fansalsoconnect.apps.artistgraph import models


too_door = "536BYVgOnRky0xjsPT96zl"
coldplay = "4gzpq5DPGxSnKTe4SA8HAU"

class SpotifyHandler:
    def __init__(self):
        with open(os.getcwd() + "\\token.json") as f:
            data = json.load(f)
        client_id = data['client_id']
        client_secret = data['client_secret']
        token = tk.request_client_token(client_id=client_id, client_secret=client_secret)
        self.tk_spotify = tk.Spotify(token)

    def get_starting_artist(self):
        artist = self.create_artist(too_door, *self.get_artist_data(too_door))
        related_artists_data = self.get_related_artists_data(too_door)
        for (id, name, url) in related_artists_data:
            related_artist = self.create_artist(id, name, url)
            self.add_related_artist(artist, related_artist)
        return artist

    def get_artist_data(self, artist_id):
        artist = self.tk_spotify.artist(artist_id)
        name = artist.name
        url = artist.images[0].url
        return name, url

    def get_related_artists_data(self, artist=coldplay):
        artists = self.tk_spotify.artist_related_artists(artist)
        artist_array = [(a.id, a.name, a.images[0].url) for a in artists]
        return artist_array

    ## Working with models
    def create_artist(self, id, name, url):
        artist = models.Artist(id, name, url)
        artist.save()
        return artist

    def add_related_artist(self, artist1, artist2):
        artist1.related_artists.add(artist2)
        artist1.save()


        



