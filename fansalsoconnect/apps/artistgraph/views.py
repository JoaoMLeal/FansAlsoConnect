from django.shortcuts import render
import networkx as nx
import numpy

# Create your views here.
from fansalsoconnect.apps.artistgraph.plot_handler import get_plot


def home_view(request, *args, **kwargs):
    (script, div), debug = get_plot()

    context = {'debug': debug,
               'script': script,
               'div': div,
               }

    return render(request, 'home.html', context)