from django.shortcuts import render
import networkx as nx
import numpy

# Create your views here.
from artist_graph.graph import get_plot


def home_view(request, *args, **kwargs):

    #(script, div) = bokeh_test()
    (script, div), debug = get_plot()

    context = {'debug': "0",
               'script': script,
               'div': div,
               }

    return render(request, 'home.html', context)
