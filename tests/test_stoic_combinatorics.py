import networkx as nx
from stoic.stoic_combinatorics import ExpandGraphCombinatorics


class TestConcreteExamples(object):
    def test_expand_2_activation_edges_option1(self):
        """
        edges
            U->N
            V->N

        Reactions:
            U + V + not(N) <-> U:V:N -> U  + V + N
            N -> not(N)
        """
        g = nx.DiGraph()
        g.add_node(1, name='U')
        g.add_node(2, name='V')
        g.add_node(3, name='N')
        g.add_edge(1, 3, weight=0)
        g.add_edge(2, 3, weight=0)

        # TODO re-view N and N* (probably mixed up)
        matrix_gold = [
            [-1, 1, 0],  # U
            [-1, 1, 0],  # V
            [0, 1, -1],  # N
            [-1, 0, 1],  # not(N)
            [1, -1, 0]  # U:V:N
        ]
        vector_gold = [1, 0, 0]

        result = ExpandGraphCombinatorics(g)

        print(result.matrix)
        print(matrix_gold)
        matrix_lead = result.matrix
        vector_lead = result.vector
        assert matrix_lead == matrix_gold
        assert vector_lead == vector_gold
