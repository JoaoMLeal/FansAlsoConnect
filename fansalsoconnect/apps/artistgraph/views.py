from bokeh.embed import server_document
from bokeh.document import Document
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import Button, TextInput
from bokeh.plotting import figure
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
import networkx as nx
import numpy

# Create your views here.
from fansalsoconnect.apps.artistgraph.plot_handler import PlotHandler
from fansalsoconnect.apps.artistgraph.request_type import RequestType


def spotify_graph(request: HttpRequest) -> HttpResponse:
    script = server_document(request.build_absolute_uri())
    return render(request, "embed.html", dict(script=script))


def spotify_graph_handler(doc: Document) -> None:
    plot_handler = PlotHandler()

    def playlist_input_handler(attr, old, new):
        root_layout = curdoc().get_model_by_name('main_layout')
        sub_layouts = root_layout.children
        sub_layouts[-1] = plot_handler.get_plot(RequestType.Playlist, new)

    playlist_input = TextInput(value="", title="Playlist:")
    playlist_input.on_change("value", playlist_input_handler)

    def artist_input_handler(attr, old, new):
        root_layout = curdoc().get_model_by_name('main_layout')
        sub_layouts = root_layout.children
        sub_layouts[-1] = plot_handler.get_plot(RequestType.SingleArtist, new)

    artist_input = TextInput(value="", title="Artist:")
    artist_input.on_change("value", artist_input_handler)

    doc.add_root(column(playlist_input, artist_input, plot_handler.plot, name='main_layout'))
