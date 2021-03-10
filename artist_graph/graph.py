import networkx as nx
from bokeh.io import output_file, show
from bokeh.models import (BoxZoomTool, Circle, HoverTool,
                          MultiLine, Plot, Range1d, ResetTool, ImageURL, ImageRGBA, TapTool, )
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx, figure
from bokeh.embed import components
from bokeh.events import Tap
import artist_graph.spotify as sp
import numpy
import bokeh

graph = nx.Graph()


def related_artists_graph(artist=sp.too_door):
    n = graph.number_of_nodes()

    if not (n in graph):
        graph.add_node(n, id=artist)
        n += 1

    artists = sp.get_related_artists_id(artist)
    for a in artists:
        graph.add_node(n, id=a)
        graph.add_edge(0, n)
        n += 1
    return graph


related_artists_graph()


def image_url_list(graph):
    print(graph.nodes.data(), type(graph.nodes.data()))
    return [sp.get_artist_image_url(data['id']) for (n, data) in graph.nodes.data()]


def get_plot():
    #graph = related_artists_graph()

    plot = make_plot()
    graph_renderer = from_networkx(graph, nx.spring_layout, center=(0, 0))

    plot.renderers.append(graph_renderer)

    images = ImageURL(url="url", w=0.15, h=0.15, anchor="center")
    graph_renderer.node_renderer.data_source.data["url"] = image_url_list(graph)
    graph_renderer.node_renderer.glyph = images

    return components(plot), graph_renderer.node_renderer.data_source.data


def make_plot():
    tooltips = [
        ("id", "@id"),
    ]

    plot = Plot(sizing_mode='scale_both',
                x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1),
                toolbar_location=None)
    plot.add_tools(TapTool(), HoverTool(tooltips=tooltips))
    plot.on_event(Tap, update_related_artists)

    return plot


def update_related_artists(event):
    return event
