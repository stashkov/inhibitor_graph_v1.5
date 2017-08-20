import networkx as nx
from stoic.generate_stoic import ExpandGraph


class TestStoichiometricMatrix(object):
    def test_generate_empty_stoichiometric_matrix_size_43(self):
        g = nx.DiGraph()
        g.add_nodes_from([1, 2, 3, 4])
        g.add_edge(1, 2)

        n_of_rows = len(g.nodes())
        n_of_columns = 3 * len(g.edges())
        lead = ExpandGraph.generate_empty_stoichiometric_matrix(n_of_rows, n_of_columns)
        gold = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        assert lead == gold

    def test_generate_empty_stoichiometric_matrix_size_11(self):
        lead = ExpandGraph.generate_empty_stoichiometric_matrix(1, 1)
        gold = [[0]]
        assert lead == gold

    def test_generate_empty_stoichiometric_matrix_size_00(self):
        lead = ExpandGraph.generate_empty_stoichiometric_matrix(0, 0)
        gold = list()
        assert lead == gold

#
# class TestsAddNegationOfNodes(object):
#     def test_add_negation_of_nodes(self):
#         """
#         given graph 1 - > 2
#         we need to get
#         - graph 1 -> 2
#         - additional node 3
#         - node 3 should be stored as negation of node 2
#         """
#         g = nx.DiGraph()
#         g.add_nodes_from([1, 2])
#         g.add_edge(1, 2)
#
#         g_gold = nx.DiGraph()
#         g_gold.add_nodes_from([1, 2, 3])
#         g_gold.add_edge(1, 2)
#         additional_nodes_gold = {2: 3}
#
#         additional_nodes_lead = dict()
#         graph_lead, additional_nodes_lead = \
#             ExpandGraph.add_negation_of_nodes(additional_nodes=additional_nodes_lead, graph=g)
#         assert graph_lead.edges() == g_gold.edges()
#         assert graph_lead.nodes() == g_gold.nodes()
#         assert additional_nodes_lead == additional_nodes_gold


# class TestAddCompositeNodes(object):
#     def test_add_composite_nodes(self):
#         """
#         given graph 1 - > 2
#         we need to get
#         - graph 1 -> 2
#         - additional node 3
#         - node 3 should be stored as composite of nodes 1 and 2
#         """
#         g = nx.DiGraph()
#         g.add_nodes_from([1, 2])
#         g.add_edge(1, 2, weight=0)
#
#         g_gold = nx.DiGraph()
#         g_gold.add_nodes_from([1, 2, 3])
#         g_gold.add_edge(1, 2, weight=0)
#         additional_nodes_gold = {(1, 2): 3}
#
#         additional_nodes_lead = dict()
#         graph_lead, additional_nodes_lead = \
#             ExpandGraph.add_composite_nodes(additional_nodes=additional_nodes_lead, graph=g)
#         assert graph_lead.edges() == g_gold.edges()
#         assert graph_lead.nodes() == g_gold.nodes()
#         assert additional_nodes_lead == additional_nodes_gold
