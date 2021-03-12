import networkx as nx
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import requests

import artist_graph.spotify as sp


class Graph:

    def __init__(self):
        self.graph = nx.Graph()
        self.make_related_artists_graph(sp.too_door)

    def make_related_artists_graph(self, artist):
        n = self.graph.number_of_nodes()
        if not (n in self.graph):
            self.graph.add_node(n, id=artist)
            n += 1

        artists = sp.get_related_artists_id(artist)
        for a in artists:
            self.graph.add_node(n, id=a)
            self.graph.add_edge(0, n)
            n += 1

    def image_url_list(self):
        return [sp.get_artist_image_url(data['id']) for (n, data) in self.graph.nodes.data()]

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