import unittest
import networkx as nx


class ExpandGraph(object):
    def __init__(self, graph):
        assert isinstance(graph, nx.DiGraph)
        self.graph, self.additional_nodes = ExpandGraph.expand_graph(graph)
        self.matrix = list()
        self.vector = list()
        self.initialize_matrix_and_vector()
        self.fill_in_stoichiometric_matrix()

    def initialize_matrix_and_vector(self):
        rows = len(self.graph.nodes())
        columns = 3 * len(self.graph.edges())  # TODO each activation edge gives 3 reactions, but inhibition gives 2
        self.matrix = self.generate_empty_stoichiometric_matrix(rows, columns)
        self.vector = [0 for _ in range(len(self.graph.edges()))]

    def fill_in_stoichiometric_matrix(self):
        assert all('weight' in d.keys() for u, v, d in self.graph.edges(data=True)), \
            "all nodes must have weights"
        reaction_number = 0
        for edge in self.graph.edges():
            if self.graph.get_edge_data(*edge)['weight'] == 0:
                reaction_number = self.add_activation_edge_reactions(edge, reaction_number)

    def add_activation_edge_reactions(self, edge, reaction_number):
        """
        Given edge PKA -> GRK2

        Re-write it as system of reactions:
        PKA + not(GRK2) <-> PKA:GRK2
        PKA:GRK2 -> GRK2 + PKA
        GRK2 -> not(GRK2)

        Expands it

        to stoichiometric matrix
                    reaction1    reaction2    reaction3
        PKA            -1            1           0
        not(GRK2)      -1            0           1
        GRK2            0            1          -1
        PKA:GRK2        1           -1           0

        and reversibility vector [1, 0, 0]
        """
        assert isinstance(edge, tuple)
        u, v = edge
        self.add_first_reaction(u, v, reaction_number)
        reaction_number += 1
        self.add_second_reaction(u, v, reaction_number)
        reaction_number += 1
        self.add_third_reaction(v, reaction_number)
        return reaction_number

    def add_first_reaction(self, u, v, column):
        # print("First Reaction: {} + {} <-> {}".format(u, self.additional_nodes[v], self.additional_nodes[(u, v)]))
        self.matrix[u - 1][column] = -1
        self.matrix[self.additional_nodes[v] - 1][column] = -1
        self.matrix[self.additional_nodes[(u, v)] - 1][column] = 1

    def add_second_reaction(self, u, v, column):
        # print("Second Reaction: {} -> {} + {}".format(self.additional_nodes[(u, v)], u, v))
        self.matrix[self.additional_nodes[(u, v)] - 1][column] = -1
        self.matrix[u - 1][column] = 1
        self.matrix[v - 1][column] = 1

    def add_third_reaction(self, v, column):
        # print("Third Reaction: {} -> {}".format(v, self.additional_nodes[v]))
        self.matrix[v - 1][column] = -1
        self.matrix[self.additional_nodes[v] - 1][column] = 1

    @staticmethod
    def generate_empty_stoichiometric_matrix(number_of_rows, number_of_columns):
        return [[0 for _ in range(number_of_columns)] for _ in range(number_of_rows)]

    @staticmethod
    def add_composite_nodes(additional_nodes, graph):  # TODO composite node
        next_node_number = max(graph.nodes())
        for edge in graph.edges():
            next_node_number += 1
            graph.add_node(next_node_number, label='Negation of ' + str(edge))
            additional_nodes[edge] = next_node_number
        return graph, additional_nodes

    @staticmethod
    def add_negation_of_nodes(additional_nodes, graph):
        next_node_number = max(graph.nodes())
        for node in graph.nodes():
            if graph.in_degree(node) > 0:
                next_node_number += 1
                graph.add_node(next_node_number, label='Composite of ' + str(node))
                additional_nodes[node] = next_node_number
        return graph, additional_nodes

    @staticmethod
    def expand_graph(graph):
        additional_nodes = dict()
        graph, additional_nodes = ExpandGraph.add_negation_of_nodes(additional_nodes, graph)
        graph, additional_nodes = ExpandGraph.add_composite_nodes(additional_nodes, graph)
        return graph, additional_nodes


class TestsExpansionStep(unittest.TestCase):
    # @unittest.skip("not implemented")
    def test_expand_activation_edge(self):
        g = nx.DiGraph()
        g.add_nodes_from([1, 2])
        g.add_edge(1, 2, weight=0)

        matrix_gold = [
            [-1, 1, 0],
            [0, 1, -1],
            [-1, 0, 1],
            [1, -1, 0]
        ]
        vector_gold = [1, 0, 0]

        matrix_lead = ExpandGraph(g).matrix
        vector_lead = ExpandGraph(g).vector
        self.assertEqual(matrix_lead, matrix_gold, "matrices are not the same")
        # self.assertEqual(vector_lead, vector_gold, "vectors are not the same")


class TestStoichiometricMatrix(unittest.TestCase):
    def test_generate_empty_stoichiometric_matrix_size_43(self):
        g = nx.DiGraph()
        g.add_nodes_from([1, 2, 3, 4])
        g.add_edge(1, 2)

        n_of_rows = len(g.nodes())
        n_of_columns = 3 * len(g.edges())
        lead = ExpandGraph.generate_empty_stoichiometric_matrix(n_of_rows, n_of_columns)
        gold = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(lead, gold)

    def test_generate_empty_stoichiometric_matrix_size_11(self):
        lead = ExpandGraph.generate_empty_stoichiometric_matrix(1, 1)
        gold = [[0]]
        self.assertEqual(lead, gold)

    def test_generate_empty_stoichiometric_matrix_size_00(self):
        lead = ExpandGraph.generate_empty_stoichiometric_matrix(0, 0)
        gold = list()
        self.assertEqual(lead, gold)


class TestsAddNegationOfNodes(unittest.TestCase):
    def test_add_negation_of_nodes(self):
        """
        given graph 1 - > 2
        we need to get
        - graph 1 -> 2
        - additional node 3
        - node 3 should be stored as negation of node 2
        """
        g = nx.DiGraph()
        g.add_nodes_from([1, 2])
        g.add_edge(1, 2)

        g_gold = nx.DiGraph()
        g_gold.add_nodes_from([1, 2, 3])
        g_gold.add_edge(1, 2)
        additional_nodes_gold = {2: 3}

        additional_nodes_lead = dict()
        graph_lead, additional_nodes_lead = \
            ExpandGraph.add_negation_of_nodes(additional_nodes=additional_nodes_lead, graph=g)
        self.assertEqual(graph_lead.edges(), g_gold.edges(), "edges are not the same")
        self.assertEqual(graph_lead.nodes(), g_gold.nodes(), "nodes are not the same")
        self.assertEqual(additional_nodes_lead, additional_nodes_gold, "dicts of additional nodes are not the same")


class TestAddCompositeNodes(unittest.TestCase):
    def test_add_composite_nodes(self):
        """
        given graph 1 - > 2
        we need to get
        - graph 1 -> 2
        - additional node 3
        - node 3 should be stored as composite of nodes 1 and 2
        """
        g = nx.DiGraph()
        g.add_nodes_from([1, 2])
        g.add_edge(1, 2)

        g_gold = nx.DiGraph()
        g_gold.add_nodes_from([1, 2, 3])
        g_gold.add_edge(1, 2)
        additional_nodes_gold = {(1, 2): 3}

        additional_nodes_lead = dict()
        graph_lead, additional_nodes_lead = \
            ExpandGraph.add_composite_nodes(additional_nodes=additional_nodes_lead, graph=g)
        self.assertEqual(graph_lead.edges(), g_gold.edges())
        self.assertEqual(graph_lead.nodes(), g_gold.nodes())
        self.assertEqual(additional_nodes_lead, additional_nodes_gold)
