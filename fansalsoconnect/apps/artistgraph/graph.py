import os

import networkx as nx
import requests
from PIL import Image, ImageDraw, ImageFilter
import numpy
import math

import fansalsoconnect.apps.artistgraph.spotify as sp
from fansalsoconnect.apps.artistgraph.model.artist import Artist
from fansalsoconnect.apps.artistgraph.model.graph import Graph, GraphImage

import bokeh
from bokeh.io import output_file, show
from bokeh.models import (BoxZoomTool, Circle, HoverTool,
                          MultiLine, Plot, Range1d, ResetTool, ImageURL, ImageRGBA, TapTool, StaticLayoutProvider, )
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx, figure
from bokeh.embed import components
from bokeh.events import Tap


def get_plot():
    g = Graph()

    plot = make_plot()
    graph_renderer = from_networkx(g.graph, nx.spring_layout, center=(0, 0))

    plot.renderers.append(graph_renderer)

    #images = ImageURL(url="url", w=0.15, h=0.15, anchor="center")
    #graph_renderer.node_renderer.data_source.data["url"] = g.image_url_list()

    images = ImageRGBA(image="image", x=0, y=0, dw=0.15, dh=0.15)
    graph_renderer.node_renderer.data_source.data["image"] = g.image_rgba_list()

    graph_renderer.node_renderer.glyph = images

    ### start of layout code
    node_indices = graph_renderer.node_renderer.data_source.data['index']
    graph_layout = graph_renderer.layout_provider.graph_layout

    ### Draw quadratic bezier paths
    def quad_bezier(start, end, control, steps):
        return [(1 - s) ** 2 * start + 2 * (1 - s) * s * control + s ** 2 * end for s in steps]

    def lin_bezier(start, end, steps, offset=0.075):
        return [(start + offset) + s * ((end + offset) - (start + offset)) for s in steps]

    xs, ys = [], []
    sx, sy = graph_layout[0]
    steps = [i / 100. for i in range(100)]
    for node_index in node_indices[1:]:
        ex, ey = graph_layout[node_index]
        xs.append(lin_bezier(sx, ex, steps))
        ys.append(lin_bezier(sy, ey, steps))

    graph_renderer.edge_renderer.data_source.data['xs'] = xs
    graph_renderer.edge_renderer.data_source.data['ys'] = ys

    return components(plot), "debug"


def make_plot():
    tooltips = [
        ("id", "@artist_id"),
        ("name", "@artist_name")
    ]

    plot = Plot(sizing_mode='scale_both',
                x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1),
                toolbar_location=None)
    plot.add_tools(TapTool(), HoverTool(tooltips=tooltips))
    return plot
