from bokeh.embed import server_document
from bokeh.document import Document
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.plotting import figure
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
import networkx as nx
import numpy

# Create your views here.
from fansalsoconnect.apps.artistgraph.plot_handler import get_plot


def spotify_graph(request: HttpRequest) -> HttpResponse:
    script = server_document(request.build_absolute_uri())
    return render(request, "embed.html", dict(script=script))


def spotify_graph_handler(doc: Document) -> None:
    plot = get_plot()

    p = figure(plot_width=400, plot_height=400)
    p.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)

    doc.add_root(plot)
