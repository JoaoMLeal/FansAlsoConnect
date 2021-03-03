import networkx as nx

from bokeh.io import output_file, show
from bokeh.models import (BoxZoomTool, Circle, HoverTool,
                          MultiLine, Plot, Range1d, ResetTool, ImageURL,)
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx, figure
from bokeh.embed import components

import bokeh

def bokeh_test(G):
    # Prepare Data

    plot = figure(title="Networkx Integration Demonstration", x_range=(-1.1, 1.1), y_range=(-1.1, 1.1),
                  tools="", toolbar_location=None)

    plot = Plot(plot_width=400, plot_height=400,
                x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))

    graph = from_networkx(G, nx.circular_layout, center=(0, 0))

    # print(graph.layout(plot=plot, side="x"))

    plot.renderers.append(graph)

    return components(plot)
