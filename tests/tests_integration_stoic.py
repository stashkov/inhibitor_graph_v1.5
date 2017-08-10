import unittest

import networkx as nx

from stoic.generate_stoic import ExpandGraph


class TestsExpansionStepSingleActivation(unittest.TestCase):
    def setUp(self):
        """
        activation edge 1 -> 2

        edges
            A->B

        Reactions:
            A + not(B) <-> A:B
            A:B -> A + B
            B -> not(B)
        """
        g = nx.DiGraph()
        g.add_nodes_from([1, 2])
        g.add_edge(1, 2, weight=0)

        self.matrix_gold = [
            [-1, 1, 0],  # A
            [0, 1, -1],  # B
            [-1, 0, 1],  # not(B)
            [1, -1, 0]  # A:B
        ]
        self.vector_gold = [1, 0, 0]

        result = ExpandGraph(g)
        self.matrix_lead = result.matrix
        self.vector_lead = result.vector

    def test_expand_activation_edge_matrix(self):
        self.assertEqual(self.matrix_lead, self.matrix_gold)

    def test_expand_activation_edge_vector(self):
        self.assertEqual(self.vector_lead, self.vector_gold)


class TestsExpansionStepSingleInhibition(unittest.TestCase):
    def setUp(self):
        """
        inhibition edge 1 -| 2

        edges
            A-|B

        Reactions:
            A + B <-> A:not(B)
            A:not(B) -> A + not(B)
        """
        g = nx.DiGraph()
        g.add_nodes_from([1, 2])
        g.add_edge(1, 2, weight=1)

        self.matrix_gold = [
            [-1, 1],  # A
            [-1, 0],  # B
            [0, 1],  # not(B)
            [1, -1]  # A:not(B)
        ]
        self.vector_gold = [1, 0]

        result = ExpandGraph(g)
        self.matrix_lead = result.matrix
        self.vector_lead = result.vector

    def test_expand_inhibition_edge_matrix(self):
        self.assertEqual(self.matrix_lead, self.matrix_gold)

    def test_expand_inhibition_edge_vector(self):
        self.assertEqual(self.vector_lead, self.vector_gold)


class TestsExpansionStepSingleInhibitionAndActivationSeparate(unittest.TestCase):
    def setUp(self):
        """
        two separate edges 1->2 and 3-|4

        edges
            A->B
            C-|D

        Reactions:
            A + not(B) <-> A:B
            A:B -> A + B
            B -> not(B)
            C + D <-> C:not(D)
            C:not(D) -> C + not(D)
        """
        g = nx.DiGraph()
        g.add_nodes_from([1, 2])
        g.add_edge(1, 2, weight=0)
        g.add_nodes_from([3, 4])
        g.add_edge(3, 4, weight=1)

        self.matrix_gold = [
            [-1, 1, 0, 0, 0],  # A
            [0, 1, -1, 0, 0],  # B
            [0, 0, 0, -1, 1],  # C
            [0, 0, 0, -1, 0],  # D
            [-1, 0, 1, 0, 0],  # not(B)
            [0, 0, 0, 0, 1],  # not(D)
            [1, -1, 0, 0, 0],  # A:B
            [0, 0, 0, 1, -1]  # C:not(D)
        ]
        self.vector_gold = [1, 0, 0, 1, 0]

        result = ExpandGraph(g)
        self.matrix_lead = result.matrix
        self.vector_lead = result.vector

    def test_matrix(self):
        self.assertEqual(self.matrix_lead, self.matrix_gold)

    def test_vector(self):
        self.assertEqual(self.vector_lead, self.vector_gold)


class TestsExpansionStepTwoActivationEdges(unittest.TestCase):
    def setUp(self):
        """
        edges
            A->C
            B->C

        Reactions:
            A + not(C) <-> A:C
            A:C -> A + C
            C -> not(C)
            B + not(C) <-> B:C
            B:C -> B + C
        """
        g = nx.DiGraph()
        g.add_nodes_from([1, 2, 3])
        g.add_edge(1, 3, weight=0)
        g.add_edge(2, 3, weight=0)

        self.matrix_gold = [
            [-1, 1, 0, 0, 0],  # A
            [0, 0, 0, -1, 1],  # B
            [0, 1, -1, 0, 1],  # C
            [-1, 0, 1, -1, 0],  # not(C)
            [1, -1, 0, 0, 0],  # A:C
            [0, 0, 0, 1, -1]  # B:C
        ]
        self.vector_gold = [1, 0, 0, 1, 0]

        result = ExpandGraph(g)
        self.matrix_lead = result.matrix
        self.vector_lead = result.vector

    def test_matrix(self):
        self.assertEqual(self.matrix_lead, self.matrix_gold)

    def test_vector(self):
        self.assertEqual(self.vector_lead, self.vector_gold)


class TestsExpansionStepTwoInhibitionEdges(unittest.TestCase):
    def setUp(self):
        """
        edges
            A-|C
            B-|C

        Reactions:
            A + C <-> A:not(C)
            A:not(C) -> A + not(C)
            B + C <-> B:not(C)
            B:not(C) -> B + not(C)
        """
        g = nx.DiGraph()
        g.add_nodes_from([1, 2, 3])
        g.add_edge(1, 3, weight=1)
        g.add_edge(2, 3, weight=1)

        self.matrix_gold = [
            [-1, 1, 0, 0],  # A
            [0, 0, -1, 1],  # B
            [-1, 0, -1, 0],  # C
            [0, 1, 0, 1],  # not(C)
            [1, -1, 0, 0],  # A:not(C)
            [0, 0, 1, -1]  # B:not(C)
        ]
        self.vector_gold = [1, 0, 1, 0]

        result = ExpandGraph(g)
        self.matrix_lead = result.matrix
        self.vector_lead = result.vector

    def test_matrix(self):
        self.assertEqual(self.matrix_lead, self.matrix_gold)

    def test_vector(self):
        self.assertEqual(self.vector_lead, self.vector_gold)


class TestsExpansionStepInhibitionAndActivationEdges(unittest.TestCase):
    def setUp(self):
        """
        edges
            A->C
            B-|C

        Reactions:
            A + not(C) <-> A:C
            A:C -> A + C
            C -> not(C)
            B + C <-> B:not(C)
            B:not(C) -> B + not(C)
        Nodes:
            A
            B
            C
            not(C)
            A:C
            B:not(C)

        """
        g = nx.DiGraph()
        g.add_nodes_from([1, 2, 3])
        g.add_edge(1, 3, weight=0)
        g.add_edge(2, 3, weight=1)

        self.matrix_gold = [
            [-1, 1, 0, 0, 0],  # A
            [0, 0, 0, -1, 1],  # B
            [0, 1, -1, -1, 0],  # C
            [-1, 0, 1, 0, 1],  # not(C)
            [1, -1, 0, 0, 0],  # A:C
            [0, 0, 0, 1, -1],  # B:not(C)
        ]
        self.vector_gold = [1, 0, 0, 1, 0]

        result = ExpandGraph(g)
        self.matrix_lead = result.matrix
        self.vector_lead = result.vector

    def test_matrix(self):
        self.assertEqual(self.matrix_lead, self.matrix_gold)

    def test_vector(self):
        self.assertEqual(self.vector_lead, self.vector_gold)


class TestsExpansionStepThreeActivationEdges(unittest.TestCase):
    def setUp(self):
        """
        edges
            A->C
            B->C
            D->C

        Reactions:
            A + not(C) <-> A:C
            A:C -> A + C
            C -> not(C)
            B + not(C) <-> B:C
            B:C -> B + C
            D + not(C) <-> D:C
            D:C -> D + C
        """
        g = nx.DiGraph()
        g.add_nodes_from([1, 2, 3, 4])
        g.add_edge(1, 3, weight=0)
        g.add_edge(2, 3, weight=0)
        g.add_edge(4, 3, weight=0)

        self.matrix_gold = [[-1, 1, 0, 0, 0, 0, 0],  # A
                            [0, 0, 0, -1, 1, 0, 0],  # B
                            [0, 1, -1, 0, 1, 0, 1],  # C
                            [0, 0, 0, 0, 0, -1, 1],  # D
                            [-1, 0, 1, -1, 0, -1, 0],  # not(C)
                            [1, -1, 0, 0, 0, 0, 0],  # A:C
                            [0, 0, 0, 1, -1, 0, 0],  # B:C
                            [0, 0, 0, 0, 0, 1, -1]]  # D:C
        self.vector_gold = [1, 0, 0, 1, 0, 1, 0]

        result = ExpandGraph(g)
        self.matrix_lead = result.matrix
        self.vector_lead = result.vector

    def test_matrix(self):
        self.assertEqual(self.matrix_lead, self.matrix_gold)

    def test_vector(self):
        self.assertEqual(self.vector_lead, self.vector_gold)
