import networkx as nx
import csv


class GraphReader(object):
    """
    Creates networkx DiGraph based on 2 files.
    - list of node names
    - list of edges and their weights
    """

    TEMPLATE = "{source} {target} {weight}"

    def __init__(self, input_file):
        self.input_file = input_file
        self.graph = nx.DiGraph()
        self.parsed_edge_list = list()
        self.node_names = list()
        self.seen_nodes = set()
        self.dict_names_to_numbers = dict()
        self.node_count = 0

    def read_nodes_names(self):
        for node_name, node_number in self.dict_names_to_numbers.items():
            self.graph.add_node(node_number, name=node_name)

    def create_graph(self):
        """generate a graph from edge list (as in python list)"""
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
            for row in edgelist:
                self.check_row_length(row)
                source, target, weight = [i.rstrip() for i in row]
                weight = self.convert_weight_to_int(weight)
                self.populate_dict(source, target)

                self.parsed_edge_list.append(self.TEMPLATE.format(source=self.dict_names_to_numbers[source],
                                                                  target=self.dict_names_to_numbers[target],
                                                                  weight=weight))

    def populate_dict(self, source, target):
        for node in [source, target]:
            if node not in self.seen_nodes:
                self.node_count += 1
                self.seen_nodes.add(node)
                self.dict_names_to_numbers[node] = self.node_count

    @staticmethod
    def check_row_length(row):
        if len(row) != 3:
            raise ValueError(
                "Each row should have exactly 3 elements, but row: {} has {} elements".format(row, len(row)))

    @staticmethod
    def convert_weight_to_int(weight):
        if weight.lower() == 'ACTIVATION'.lower():
            return 0
        elif weight.lower() == 'INHIBITION'.lower():
            return 1
        else:
            raise ValueError("Only ACTIVATION and INHIBITION allowed, but you supplied {}".format(weight))
