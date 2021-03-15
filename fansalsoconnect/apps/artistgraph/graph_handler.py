import networkx as nx
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import requests

import fansalsoconnect.apps.artistgraph.spotify_handler as sp
import fansalsoconnect.apps.artistgraph.models as models


class GraphHandler:

    def __init__(self):
        self.graph = nx.Graph()
        self.spotify_handler = sp.SpotifyHandler()
        self.make_starting_graph()


    def make_starting_graph(self):
        n = 0
        artist = self.spotify_handler.get_starting_artist()
        self.graph.add_node(n, artist_id=artist.id, artist_name=artist.name, artist_url=artist.image_url)
        n += 1

        artists = artist.related_artists.all()
        for a in artists:
            self.graph.add_node(n, artist_id=a.id, artist_name=a.name, artist_url=a.image_url)
            self.graph.add_edge(0, n)
            n += 1


    def image_url_list(self):
        all_artists = models.Artist.objects.all()
        return [artist.image_url for artist in all_artists]

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