from django.shortcuts import render
import networkx as nx
import artist_graph.spotify as spotify
import numpy

# Create your views here.
from artist_graph.graph import bokeh_test


def home_view(request, *args, **kwargs):

    img = spotify.get_image("536BYVgOnRky0xjsPT96zl")

    G1 = nx.Graph()
    G1.add_node(1)#, image=numpy.array(img))
    G1.add_nodes_from([2, 3])
    G1.add_edge(1, 2)
    G1.add_edges_from([(1, 3)])

    nodePos = nx.random_layout(G1)
    nx.set_node_attributes(G1, nodePos, "pos")

    script, div = bokeh_test(G1)

    context = {'world': 'world',
               'script': script,
               'div': div,
               'album': spotify.spotify_stuff(),
               }

    return render(request, 'home.html', context)
