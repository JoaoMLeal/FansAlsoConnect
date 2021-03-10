import networkx as nx

from bokeh.io import output_file, show
from bokeh.models import (BoxZoomTool, Circle, HoverTool,
                          MultiLine, Plot, Range1d, ResetTool, ImageURL, ImageRGBA, )
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx, figure
from bokeh.embed import components

from artist_graph.spotify import get_image

import numpy

import bokeh


def bokeh_test(G):
    # Prepare Data

    plot = Plot(sizing_mode='scale_both', x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1),
                toolbar_location=None)

    graph_renderer = from_networkx(G, nx.circular_layout, center=(0, 0))

    plot.renderers.append(graph_renderer)

    # im = get_image()
    # im = im.convert("RGBA")
    # imarray = numpy.array(im)

    image3 = ImageURL(url="url", w=0.1, h=0.1, anchor="center")
    graph_renderer.node_renderer.data_source.data["url"] = [get_image()]*3
    graph_renderer.node_renderer.glyph = image3

    return components(plot), plot
