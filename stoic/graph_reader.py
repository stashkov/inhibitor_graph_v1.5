import networkx as nx


class GraphReader(object):
    """
    Creates networkx DiGraph based on 2 files.
    - list of node names
    - list of edges and their weights
    """

    def __init__(self, node_names, edge_list):
        self.node_names = node_names
        self.edge_list = edge_list
        self.graph = nx.DiGraph()

    def read_nodes_names(self):
        with open(self.node_names, 'r') as f:
            for i, line in enumerate(f, start=1):
                line = line.rstrip()
                if line:
                    self.graph.add_node(i, name=line)
                else:
                    raise ValueError('Line %s in the file %s must not be empty' %
                                     (i, self.node_names))

    def create_graph(self):
        self.graph = nx.read_edgelist(self.edge_list, nodetype=int, create_using=nx.DiGraph(), data=(('weight', int),))
        self.read_nodes_names()
        return self.graph
