import networkx as nx

from stoic.stoic import ExpandGraph


class TestSizeOfStoichiometricMatrix(object):
    def test_size_stoichiometric(self):
        g = nx.DiGraph()
        g.add_nodes_from([1, 2])
        g.add_edge(1, 2, weight=0)
        result = ExpandGraph(g)
        assert len(result.matrix) == 4

    def test_size_stoichiometric1(self):
        g = nx.DiGraph()
        g.add_nodes_from([1, 2])
        g.add_edge(1, 2, weight=1)
        result = ExpandGraph(g)
        assert len(result.matrix) == 4


class TestConcreteExamples(object):
    def test_expand_activation_edge(self):
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

        matrix_gold = [
            [-1, 1, 0],  # A
            [0, 1, -1],  # B
            [-1, 0, 1],  # not(B)
            [1, -1, 0]  # A:B
        ]
        vector_gold = [1, 0, 0]

        result = ExpandGraph(g)
        matrix_lead = result.matrix
        vector_lead = result.vector
        assert matrix_lead == matrix_gold
        assert vector_lead == vector_gold

    def test_expand_inhibition_edge(self):
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

        matrix_gold = [
            [-1, 1],  # A
            [-1, 0],  # B
            [0, 1],  # not(B)
            [1, -1]  # A:not(B)
        ]
        vector_gold = [1, 0]

        result = ExpandGraph(g)
        matrix_lead = result.matrix
        vector_lead = result.vector

        assert matrix_lead == matrix_gold
        assert vector_lead == vector_gold

    def test_activation_and_inhibition_edges_separately(self):
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

        matrix_gold = [
            [-1, 1, 0, 0, 0],  # A
            [0, 1, -1, 0, 0],  # B
            [0, 0, 0, -1, 1],  # C
            [0, 0, 0, -1, 0],  # D
            [-1, 0, 1, 0, 0],  # not(B)
            [0, 0, 0, 0, 1],  # not(D)
            [1, -1, 0, 0, 0],  # A:B
            [0, 0, 0, 1, -1]  # C:not(D)
        ]
        vector_gold = [1, 0, 0, 1, 0]

        result = ExpandGraph(g)
        matrix_lead = result.matrix
        vector_lead = result.vector

        assert matrix_lead == matrix_gold
        assert vector_lead == vector_gold

    def test_two_activation_edges_together(self):
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

        matrix_gold = [
            [-1, 1, 0, 0, 0],  # A
            [0, 0, 0, -1, 1],  # B
            [0, 1, -1, 0, 1],  # C
            [-1, 0, 1, -1, 0],  # not(C)
            [1, -1, 0, 0, 0],  # A:C
            [0, 0, 0, 1, -1]  # B:C
        ]
        vector_gold = [1, 0, 0, 1, 0]

        result = ExpandGraph(g)
        matrix_lead = result.matrix
        vector_lead = result.vector

        assert matrix_lead == matrix_gold
        assert vector_lead == vector_gold

    def test_two_inhibition_edges_together(self):
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

        matrix_gold = [
            [-1, 1, 0, 0],  # A
            [0, 0, -1, 1],  # B
            [-1, 0, -1, 0],  # C
            [0, 1, 0, 1],  # not(C)
            [1, -1, 0, 0],  # A:not(C)
            [0, 0, 1, -1]  # B:not(C)
        ]
        vector_gold = [1, 0, 1, 0]

        result = ExpandGraph(g)
        matrix_lead = result.matrix
        vector_lead = result.vector

        assert matrix_lead == matrix_gold
        assert vector_lead == vector_gold

    def test_inhibition_and_activation_edges_together(self):
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

        matrix_gold = [
            [-1, 1, 0, 0, 0],  # A
            [0, 0, 0, -1, 1],  # B
            [0, 1, -1, -1, 0],  # C
            [-1, 0, 1, 0, 1],  # not(C)
            [1, -1, 0, 0, 0],  # A:C
            [0, 0, 0, 1, -1],  # B:not(C)
        ]
        vector_gold = [1, 0, 0, 1, 0]

        result = ExpandGraph(g)
        matrix_lead = result.matrix
        vector_lead = result.vector
        assert matrix_lead == matrix_gold
        assert vector_lead == vector_gold

    def test_three_activation_edges_together(self):
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

        matrix_gold = [[-1, 1, 0, 0, 0, 0, 0],  # A
                       [0, 0, 0, -1, 1, 0, 0],  # B
                       [0, 1, -1, 0, 1, 0, 1],  # C
                       [0, 0, 0, 0, 0, -1, 1],  # D
                       [-1, 0, 1, -1, 0, -1, 0],  # not(C)
                       [1, -1, 0, 0, 0, 0, 0],  # A:C
                       [0, 0, 0, 1, -1, 0, 0],  # B:C
                       [0, 0, 0, 0, 0, 1, -1]]  # D:C
        vector_gold = [1, 0, 0, 1, 0, 1, 0]

        result = ExpandGraph(g)
        matrix_lead = result.matrix
        vector_lead = result.vector
        assert matrix_lead == matrix_gold
        assert vector_lead == vector_gold

    def test_reconstruct_stoic_from_reactions(self):
        g = nx.DiGraph()
        g.add_node(1, name='U')
        g.add_node(2, name='V')
        g.add_node(3, name='N')
        g.add_edge(1, 3, weight=0)
        g.add_edge(2, 3, weight=0)
        result = ExpandGraph(g)
        matrix_lead = result.matrix

        matrix_gold = [
            [-1, 1, 0, 0, 0],  # A
            [0, 0, 0, -1, 1],  # B
            [0, 1, -1, 0, 1],  # C
            [-1, 0, 1, -1, 0],  # not(C)
            [1, -1, 0, 0, 0],  # A:C
            [0, 0, 0, 1, -1]  # B:C
        ]
        assert matrix_lead == matrix_gold
