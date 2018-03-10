import json
import pprint
import argparse
import numpy as np
import networkx as nx

from itertools import repeat

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# class Layer:
#
#     def __init__(self, id):
#         self.id = id
#
#
#     @property
#     def id(self):
#         return self._id
#
#     @id.setter
#     def id(self, v):
#         self._id = v
#
#


def gen_net_graph():

    Net = nx.MultiDiGraph()
    # add 4 nodes + (input, out)
    Net.add_nodes_from(np.arange(6) + 1)

    # Layer relationships
    Net.add_edge(1,2, layer = 1)
    Net.add_edge(2,1, layer = 1)

    Net.add_edge(3,4, layer = 2)
    Net.add_edge(4,3, layer = 2)

    # Node axons
    Net.add_edge(1, 3, axon = True)
    Net.add_edge(1, 4, axon = True)
    Net.add_edge(2, 4, axon = True)



    # Input reference
    in_edges = filter_edge(Net, 'layer', val = 1)[:, 0]
    h = np.zeros((in_edges.shape[0], 2)).astype(int)
    h[:, 0] = 5
    h[:, 1] = in_edges
    Net.add_edges_from(h, input = True)

    # Output reference
    out_edges = filter_edge(Net, 'layer', val = 2)[:, 0]
    h = np.zeros((out_edges.shape[0], 2)).astype(int)
    h[:, 0] = out_edges
    h[:, 1] = 6
    Net.add_edges_from(h, output = True)

    return Net

def filter_edge(g, data, val = None):
    t = np.vstack(g.edges(data = data, default = False))
    v = t[np.where(t[:, 2])]

    if not val is None:
        v = v[np.where(v[:, 2] == val)]
    return v


def plot_net(net, path):
    fig, ax =  plt.subplots(1, 1)
    axons = filter_edge(net, 'axon')
    layers = filter_edge(net, 'layer')
    n_layers = len(np.unique(layers[:, 2]))
    n_nodes = len(net.nodes())

    inpt = filter_edge(net, 'input')
    output = filter_edge(net, 'output')

    # colors = np.hstack(
    #     (np.repeat('r', len(axons)), np.repeat('b', len(layers)),
    #      np.repeat('y', len(inpt)), np.repeat('g', len(output))))

    colors = np.hstack(
        (np.repeat('r', len(axons)), np.repeat('y', len(inpt)),
        np.repeat('g', len(output))))

    edges = np.vstack((axons, inpt, output))
    # edges = np.vstack((axons, layers, inpt, output))

    pos = {}
    for row in range(n_layers):
        layer = layers[np.where(layers[:, 2] == row + 1)][:, 0]
        for col in range(len(layer)):
            node = layer[col]
            pos[node] = (col, row + 1)
    pos[(n_nodes - 1)] = (0, 0)
    pos[n_nodes] = (0, n_layers + 1)


    nx.draw(net, edgelist = edges.tolist(), edge_color = colors, pos = pos,
        ax= ax)
    fig.savefig(path)


def main():

    net = gen_net_graph()
    plot_net(net, 'graph_plot')


if __name__ == '__main__':
    main()
