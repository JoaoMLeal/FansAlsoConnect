import os

import networkx as nx
import requests
from PIL import Image, ImageDraw, ImageFilter
import numpy
import math

from fansalsoconnect.apps.artistgraph.graph_handler import GraphHandler, GraphImage

import bokeh
from bokeh.io import output_file, show
from bokeh.models import (BoxZoomTool, Circle, HoverTool,
                          MultiLine, Plot, Range1d, ResetTool, ImageURL, ImageRGBA, TapTool, StaticLayoutProvider,
                          CustomJS, )
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx, figure
from bokeh.embed import components
from bokeh.events import Tap


def get_plot():
    gh = GraphHandler()

    plot = make_plot()
    graph_renderer = from_networkx(gh.graph, nx.spring_layout, center=(0, 0))
    plot.renderers.append(graph_renderer)

    node_images(graph_renderer, gh)
    make_edges(graph_renderer)

    return components(plot), "debug"


def make_plot():
    callback = CustomJS(code="""
    console.log("Aaaa ");
    """)
    tap_tool = TapTool(callback=callback)

    hover_tool = HoverTool(tooltips = [
        ("id", "@artist_id"),
        ("name", "@artist_name")
    ])

    plot = Plot(sizing_mode='scale_both',
                x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1),
                toolbar_location=None)
    plot.add_tools(tap_tool, hover_tool)
    return plot


def node_images(graph_renderer, graph):
    images = ImageRGBA(image="image", x=0, y=0, dw=0.15, dh=0.15)
    graph_renderer.node_renderer.data_source.data["image"] = graph.image_rgba_list()
    graph_renderer.node_renderer.glyph = images


def make_edges(graph_renderer):
    node_indices = graph_renderer.node_renderer.data_source.data['index']
    graph_layout = graph_renderer.layout_provider.graph_layout

    ### Draw linear bezier paths
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