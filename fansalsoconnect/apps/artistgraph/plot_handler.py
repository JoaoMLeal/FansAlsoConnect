import os

import networkx as nx
import requests
from PIL import Image, ImageDraw, ImageFilter
import numpy
import math

from fansalsoconnect.apps.artistgraph.graph_handler import GraphHandler, GraphImage
from fansalsoconnect.apps.artistgraph.request_type import RequestType

import bokeh
from bokeh.io import output_file, show, curdoc
from bokeh.models import (BoxZoomTool, Circle, HoverTool,
                          MultiLine, Plot, Range1d, ResetTool, ImageURL, ImageRGBA, TapTool, StaticLayoutProvider,
                          CustomJS, NodesAndLinkedEdges, NodesOnly, Button, ColumnDataSource, GraphRenderer,
                          WheelZoomTool, PanTool, )
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx, figure
from bokeh.embed import components
from bokeh.events import Tap
from functools import partial

PLOT_SCALE = 1
PLOT_RANGE = 1.1
PLOT_LAYOUT = nx.spring_layout
PLOT_GLYPH_SIZE = 0.02

class PlotHandler:

    def __init__(self):
        self.graph_handler = GraphHandler(RequestType.Empty)
        self.plot = self.empty_plot()

    def get_plot(self, type, id):
        print(type, id)
        self.graph_handler = GraphHandler(type, id)

        graph_renderer = from_networkx(self.graph_handler.graph, PLOT_LAYOUT, center=(0, 0), scale=PLOT_SCALE)

        self.plot.renderers[0] = graph_renderer

        self.node_images()
        self.make_edges()
        return self.plot

    def empty_plot(self):
        hover_tool = HoverTool(tooltips=[
            ("id", "@artist_id"),
            ("name", "@artist_name")
        ])
        wheel_zoom_tool = WheelZoomTool()
        reset_tool = ResetTool()
        pan_tool = PanTool()

        plot = Plot(sizing_mode='scale_both', max_height=1000, max_width=1000,
                    x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1),
                    outline_line_color=None, name='main_plot',
                    toolbar_location=None, output_backend="webgl")
        plot.add_tools(hover_tool, wheel_zoom_tool, reset_tool, pan_tool)
        plot.toolbar.active_scroll = wheel_zoom_tool

        graph_renderer = from_networkx(self.graph_handler.graph, PLOT_LAYOUT, center=(0, 0), scale=PLOT_SCALE)
        plot.renderers.append(graph_renderer)

        return plot


    def node_images(self):
        graph_renderer = self.plot.renderers[0]
        images = ImageRGBA(image="image", x=0, y=0, dw=PLOT_GLYPH_SIZE, dh=PLOT_GLYPH_SIZE)

        artist_urls = graph_renderer.node_renderer.data_source.data['artist_url']
        graph_renderer.node_renderer.data_source.data["image"] = self.graph_handler.image_rgba_list(artist_urls)

        # images = ImageURL(url="url", x=0, y=0, w=0.1, h=0.1, anchor="center")
        # graph_renderer.node_renderer.data_source.data["url"] = graph.image_url_list()

        graph_renderer.node_renderer.glyph = images


    def make_edges(self):
        graph_renderer = self.plot.renderers[0]
        node_indices = graph_renderer.node_renderer.data_source.data['index']
        graph_layout = graph_renderer.layout_provider.graph_layout
        graph = self.graph_handler.graph

        ### Draw linear bezier paths
        def lin_bezier(start, end, steps, offset=PLOT_GLYPH_SIZE/2):
            return [(start + offset) + s * ((end + offset) - (start + offset)) for s in steps]

        xs, ys = [], []
        steps = [i / 50. for i in range(50)]
        for node_index in node_indices:
            x1, y1 = graph_layout[node_index]
            edges = graph.edges(node_index)
            for _, r_index in edges:
                x2, y2 = graph_layout[r_index]
                xs.append(lin_bezier(x1, x2, steps))
                ys.append(lin_bezier(y1, y2, steps))

        graph_renderer.edge_renderer.data_source.data['xs'] = xs
        graph_renderer.edge_renderer.data_source.data['ys'] = ys
