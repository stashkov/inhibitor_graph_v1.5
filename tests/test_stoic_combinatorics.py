import networkx as nx
from stoic.stoic_combinatorics import ExpandGraphCombinatorics


class TestConcreteExamples(object):
    def setup_method(self, method):
        print("Starting execution of: {}".format(method.__name__))
        self.graph = nx.DiGraph()
        self.graph.add_node(1, name='U')
        self.graph.add_node(2, name='V')
        self.graph.add_node(3, name='N')

    def test_expand_2_activation_edges_complex(self):
        """
        edges
            U->N
            V->N

        Reactions:
            U + V + not(N) <-> U:V:N -> U + V + N
            N -> not(N)
        """
        self.graph.add_edge(1, 3, weight=0)
        self.graph.add_edge(2, 3, weight=0)

        matrix_gold = [
            [-1, 1, 0],  # U
            [-1, 1, 0],  # V
            [0, 1, -1],  # N
            [-1, 0, 1],  # not(N)
            [1, -1, 0]  # U:V:N
        ]
        vector_gold = [1, 0, 0]
        result = ExpandGraphCombinatorics(self.graph)
        assert result.matrix == matrix_gold
        assert result.vector == vector_gold

    def test_expand_mixed_reaction(self):
        """
        Mix Edges:
            U -| N
            V -> N
        Separate:
            U + N <-> U:N -> U + not(N)
            N -> not(N)
            V + N <-> V:N -> V + N
        """
        self.graph.add_edge(1, 3, weight=1)
        self.graph.add_edge(2, 3, weight=0)

        matrix_gold = [
            [-1, 1, 0, 0, 0],  # U
            [0, 0, 0, -1, 1],  # V
            [-1, 0, -1, -1, 1],  # N
            [0, 1, 1, 0, 0],  # not(N)
            [1, -1, 0, 0, 0],  # U:N
            [0, 0, 0, 1, -1]  # V:N
        ]
        vector_gold = [1, 0, 0, 1, 0]
        result = ExpandGraphCombinatorics(self.graph)
        assert result.matrix == matrix_gold
        assert result.vector == vector_gold
