import os

import networkx as nx
import requests
from PIL import Image, ImageDraw, ImageFilter
import numpy
import math

from fansalsoconnect.apps.artistgraph.graph_handler import GraphHandler, GraphImage

import bokeh
from bokeh.io import output_file, show, curdoc
from bokeh.models import (BoxZoomTool, Circle, HoverTool,
                          MultiLine, Plot, Range1d, ResetTool, ImageURL, ImageRGBA, TapTool, StaticLayoutProvider,
                          CustomJS, )
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx, figure
from bokeh.embed import components
from bokeh.events import Tap
from functools import partial

def get_plot():
    gh = GraphHandler()

    plot = make_plot()
    graph_renderer = from_networkx(gh.graph, nx.spring_layout, center=(0, 0))
    plot.renderers.append(graph_renderer)

    node_images(graph_renderer, gh)
    make_edges(graph_renderer)

    print(graph_renderer.node_renderer)
    print(graph_renderer.edge_renderer)

    return plot


def make_plot():

    tap_tool = TapTool()
    hover_tool = HoverTool(tooltips = [
        ("id", "@artist_id"),
        ("name", "@artist_name")
    ])

    plot = Plot(sizing_mode='scale_both', max_height=1000, max_width=1000,
                x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1),
                toolbar_location=None, outline_line_color=None)
    plot.add_tools(tap_tool, hover_tool)
    part = partial(print_on_click, plot)
    plot.on_event(Tap, part)
    return plot


def node_images(graph_renderer, graph):
    images = ImageRGBA(image="image", x=0, y=0, dw=0.15, dh=0.15)
    graph_renderer.node_renderer.data_source.data["image"] = graph.image_rgba_list()

    # images = ImageURL(url="url", x=0, y=0, w=0.1, h=0.1, anchor="center")
    # graph_renderer.node_renderer.data_source.data["url"] = graph.image_url_list()

    graph_renderer.node_renderer.glyph = images


def make_edges(graph_renderer):
    node_indices = graph_renderer.node_renderer.data_source.data['index']
    graph_layout = graph_renderer.layout_provider.graph_layout

    ### Draw linear bezier paths
    def lin_bezier(start, end, steps, offset=0.075):
        return [(start + offset) + s * ((end + offset) - (start + offset)) for s in steps]

    def lin_test(start, end, offset=0.075):
        return (start + offset) - ((end + offset) - (start + offset))

    xs, ys = [], []
    sx, sy = graph_layout[0]
    steps = [i / 100. for i in range(100)]
    for node_index in node_indices[1:]:
        ex, ey = graph_layout[node_index]
        xs.append(lin_bezier(sx, ex, steps))
        ys.append(lin_bezier(sy, ey, steps))

    graph_renderer.edge_renderer.data_source.data['xs'] = xs
    graph_renderer.edge_renderer.data_source.data['ys'] = ys


def print_on_click(plot, event):
    print("aaaa", event, plot.renderers[0])
