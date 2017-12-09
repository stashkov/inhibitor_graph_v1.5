import random
import string

import networkx as nx


class Barabasi(object):
    @staticmethod
    def generate_name():
        for first_letter in string.ascii_uppercase:
            for second_letter in string.ascii_uppercase:
                for third_letter in string.ascii_uppercase:
                    yield first_letter + second_letter + third_letter

    @staticmethod
    def generate(nodes=10):
        graph = nx.barabasi_albert_graph(nodes, 2, seed=13)
        assert isinstance(graph, nx.Graph)
        forward_edges = graph.edges()
        graph = graph.to_directed()
        assert isinstance(graph, nx.DiGraph)
        extra_edges = list(set(graph.edges()) - set(forward_edges))

        graph.remove_edges_from(extra_edges)

        for edge in graph.edges():
            u, v = edge
            if random.uniform(0, 1) < 0.3:
                graph[u][v]['weight'] = 1
            else:
                graph[u][v]['weight'] = 0

        for node, name in zip(graph.nodes(), Barabasi.generate_name()):
            graph.add_node(node, name=name)

        graph.remove_node(0)
        return graph
