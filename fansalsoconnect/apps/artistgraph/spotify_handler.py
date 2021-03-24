import os
from io import BytesIO
import json
import tekore as tk
import requests
from PIL import Image

from fansalsoconnect.apps.artistgraph import models


too_door = "536BYVgOnRky0xjsPT96zl"
coldplay = "4gzpq5DPGxSnKTe4SA8HAU"
playlist = "27eLNxgdRgKOQSSL6CsSF8"
playlist_test = "4tOyoJiDHuLf5tZmAJ2IZT"

class SpotifyHandler:
    def __init__(self):
        with open(os.getcwd() + "\\token.json") as f:
            data = json.load(f)
        client_id = data['client_id']
        client_secret = data['client_secret']
        token = tk.request_client_token(client_id=client_id, client_secret=client_secret)
        self.tk_spotify = tk.Spotify(token)
        self.index = 0

    def get_single_artist(self, artist_id):
        artist = self.create_artist(artist_id, *self.get_artist_data(artist_id))
        related_artists_data = self.get_related_artists_data(artist_id)
        for (id, name, url) in related_artists_data:
            related_artist = self.create_artist(id, name, url)
            self.add_related_artist(artist, related_artist)
        return artist

    def get_artist_data(self, artist_id):
        artist = self.tk_spotify.artist(artist_id)
        name = artist.name
        url = self.get_artist_image(artist)
        return name, url

    def get_related_artists_data(self, artist_id):
        artists = self.tk_spotify.artist_related_artists(artist_id)
        artist_array = [(a.id, a.name, self.get_artist_image(a)) for a in artists]
        return artist_array

    ## Working with models
    def create_artist(self, id, name, url):
        query = models.Artist.objects.filter(id=id)
        if query.exists():
            return query[0]
        else:
            artist = models.Artist(id=id, name=name, image_url=url, index=self.index)
            artist.save()
            self.index += 1
            return artist

    def add_related_artist(self, artist1, artist2):
        artist1.related_artists.add(artist2)
        artist1.save()


    def get_playlist_artists(self, playlist_id):
        artists = []
        for item in self.tk_spotify.playlist_items(playlist_id).items:
            for a in item.track.artists:
                full_artist = self.tk_spotify.artist(a.id)
                artist = self.create_artist(full_artist.id, full_artist.name, self.get_artist_image(full_artist))
                if artist not in artists:
                    artists.append(artist)
                related_artists = self.get_related_artists_data(a.id)
                for (ra_id, ra_name, ra_url) in related_artists:
                    related_artist = self.create_artist(ra_id, ra_name, ra_url)
                    if related_artist not in artists:
                        artists.append(related_artist)
                    self.add_related_artist(artist, related_artist)
        return artists


    def get_artist_image(self, artist):
        images = artist.images
        if images:
            return images[2].url
        else:
            return self.tk_spotify.artist_albums(artist.id).items[0].images[2].url



        



