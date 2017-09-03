import networkx as nx
import csv


class GraphReader(object):
    """
    Creates networkx DiGraph based on 2 files.
    - list of node names
    - list of edges and their weights
    """

    def __init__(self, input_file):
        self.input_file = input_file
        self.graph = nx.DiGraph()
        self.parsed_edge_list = list()
        self.node_names = list()
        self.seen_nodes = set()
        self.node_numbers = dict()

    def read_nodes_names(self):
        for node_name, node_number in self.node_numbers.items():
            self.graph.add_node(node_number, name=node_name)

    def create_graph(self):
        self.parse_graph()
        self.graph = nx.parse_edgelist(self.parsed_edge_list,
                                       nodetype=int,
                                       create_using=nx.DiGraph(),
                                       data=(('weight', int),))
        self.read_nodes_names()
        return self.graph

    def parse_graph(self):
        with open(self.input_file, 'r') as csvfile:
            edgelist = csv.reader(csvfile, delimiter=',', quotechar='"')
            node_count = 0
            for row in edgelist:
                if len(row) != 3:
                    raise ValueError(
                        "Each row should have exactly 3 elements, but row: {} has {} elements".format(row, len(row)))
                source, target, weight = [i.rstrip() for i in row]
                weight = GraphReader.convert_weight_to_int(weight)
                for node in [source, target]:
                    if node not in self.seen_nodes:
                        node_count += 1
                        self.seen_nodes.add(node)
                        self.node_numbers[node] = node_count
                self.parsed_edge_list.append("{source} {target} {weight}".format(source=self.node_numbers[source],
                                                                                 target=self.node_numbers[target],
                                                                                 weight=weight))

    @staticmethod
    def convert_weight_to_int(weight):
        if weight.lower() == 'ACTIVATION'.lower():
            return 0
        elif weight.lower() == 'INHIBITION'.lower():
            return 1
        else:
            raise ValueError("Only ACTIVATION and INHIBITION allowed, but you supplied {}".format(weight))
