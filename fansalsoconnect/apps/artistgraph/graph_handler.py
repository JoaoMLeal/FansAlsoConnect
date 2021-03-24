import networkx as nx
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import requests
import matplotlib.pyplot as plt

import fansalsoconnect.apps.artistgraph.spotify_handler as sp
import fansalsoconnect.apps.artistgraph.models as models
from fansalsoconnect.apps.artistgraph.request_type import RequestType


class GraphHandler:

    def __init__(self, type, id=""):
        self.graph = nx.Graph()
        self.spotify_handler = sp.SpotifyHandler()

        if type == RequestType.Empty:
            pass
        elif type == RequestType.SingleArtist:
            self.make_single_artist_graph(id)
        elif type == RequestType.Playlist:
            self.make_playlist_graph(id)


    def get_artist_ids(self):
        return [id for node, id in self.graph.nodes(data='artist_id')]


    def make_single_artist_graph(self, artist_id):
        artist = self.spotify_handler.get_single_artist(artist_id)
        self.graph.add_node(artist.index, artist_id=artist.id, artist_name=artist.name, artist_url=artist.image_url)

        related_artists = artist.related_artists.all()
        for ra in related_artists:
            self.graph.add_node(ra.index, artist_id=ra.id, artist_name=ra.name, artist_url=ra.image_url)
            self.graph.add_edge(artist.index, ra.index)

    def make_playlist_graph(self, playlist_id):
        artists = self.spotify_handler.get_playlist_artists(playlist_id)
        for a in artists:
            self.graph.add_node(a.index, artist_id=a.id, artist_name=a.name, artist_url=a.image_url)
            for ra in a.related_artists.all():
                self.graph.add_node(ra.index, artist_id=ra.id, artist_name=ra.name, artist_url=ra.image_url)
                self.graph.add_edge(a.index, ra.index)
                print(a.name, ra.name)

        fig = plt.figure(figsize=(12, 12))
        nx.draw(self.graph, nx.spring_layout(self.graph))
        plt.tight_layout()
        plt.savefig("Graph.png", format="PNG")


    def image_url_list(self):
        artist_ids = self.get_artist_ids()
        graph_artists = models.Artist.objects.filter(pk__in=artist_ids)
        return [artist.image_url for artist in graph_artists]

    def image_rgba_list(self):
        urls = self.image_url_list()
        rgbas = [GraphImage(url).to_rgba_array() for url in urls]
        return rgbas


class GraphImage:

    def __init__(self, url):
        self.url = url
        self.image = Image.open(requests.get(url, stream=True).raw)

    def mask_circle_solid(self, background_color=(0, 0, 0), blur_radius=0, offset=0):
        background = Image.new(self.image.mode, self.image.size, background_color)
        offset = blur_radius * 2 + offset
        mask = Image.new("L", self.image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((offset, offset, self.image.size[0] - offset, self.image.size[1] - offset), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

        self.image = Image.composite(self.image, background, mask)

    def mask_circle_transparent(self, blur_radius=0, offset=0):
        offset = blur_radius * 2 + offset
        mask = Image.new("L", self.image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((offset, offset, self.image.size[0] - offset, self.image.size[1] - offset), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

        result = self.image.copy()
        result.putalpha(mask)

        self.image = result

    def to_rgba_array(self):
        self.mask_circle_transparent()
        pil_img = self.image.convert('RGBA')
        xdim, ydim = pil_img.size

        img = np.empty((ydim, xdim), dtype=np.uint32)
        view = img.view(dtype=np.uint8).reshape((ydim, xdim, 4))
        view[:, :, :] = np.flipud(np.asarray(pil_img))
        return img