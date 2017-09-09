from collections import namedtuple
import itertools
import networkx as nx


class Reaction(namedtuple("Reaction", "reactants, products, reversible")):
    __slots__ = ()

    def __new__(cls, reactants, products, reversible):
        Reaction.assert_types(products, reactants, reversible)
        # noinspection PyArgumentList
        self = super(Reaction, cls).__new__(cls, reactants, products, reversible)
        return self

    @staticmethod
    def assert_types(products, reactants, reversible):
        for reagents in [reactants, products]:
            assert isinstance(reagents, list)
            assert reagents
            assert all(isinstance(i, int) for i in reagents)
        assert isinstance(reversible, bool)


class ExpandGraph(object):
    INHIBITION = 1  # edges in a graph that have weight 1 are considered inhibition edges
    ACTIVATION = 0  # edges in a graph that have weight 0 are considered activation edges
    REACTANT = -1  # terms that are on the left in chemical equation in stoichiometric matrices denoted by -1
    PRODUCT = 1  # terms that are on the right in chemical equation in stoichiometric matrices denoted by -1
    REVERSIBLE_REACTION = True  # reaction that is reversible in reversibility vector
    IRREVERSIBLE_REACTION = False
    REACTION = Reaction

    def __init__(self, graph):
        assert isinstance(graph, nx.DiGraph)
        assert all('weight' in d.keys() for _, _, d in graph.edges(data=True)), \
            "all edges must have weights"
        self.graph = graph
        self.additional_nodes = dict()
        self.expand_graph()

        self.backward_reactions = list()  # N -> N*
        self.matrix = list()  # stoichiometric matrix
        self.vector = list()
        self.reactions = list()
        self.deleted_rows_count = 0
        self.reaction_number = 0

        self.add_reactions()
        self.reconstruct_stoic_matrix_from_reactions()

    def add_reactions(self):
        for i, edge in enumerate(sorted(self.graph.edges())):
            self.add_activation_reactions(edge)
            self.add_inhibition_reactions(edge)

    def add_inhibition_reactions(self, edge):
        if self.is_inhibition_edge(edge):
            self.add_inhibition_edge_reactions(edge)

    def add_activation_reactions(self, edge):
        if self.is_activation_edge(edge):
            self.add_activation_edge_reactions(edge)

    def weight(self, edge):
        return self.graph.get_edge_data(*edge)['weight']

    def add_activation_edge_reactions(self, edge):
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
        self.add_reaction(self.first_reaction_activation(u, v))
        self.add_reaction(self.second_reaction_activation(u, v))
        if v not in self.backward_reactions:
            self.add_backward_reaction(v)

    def add_inhibition_edge_reactions(self, edge):
        """
        Given edge GRK2 -| GEF

        Re-write it as system of reactions:
        GRK2 + GEF <-> GRK2:not(GEF)
        GRK2:not(GEF) -> GRK2 + not(GEF)

        Expands it

        to stoichiometric matrix
                        reaction1    reaction2
        GRK2               -1            1
        GEF                -1            0
        not(GEF)            0            1
        GRK2:not(GEF)       1           -1

        and reversibility vector [1, 0, 0]
        """
        assert isinstance(edge, tuple)
        u, v = edge
        self.add_reaction(self.first_reaction_inhibition(u, v))
        self.add_reaction(self.second_reaction_inhibition(u, v))

    def add_reaction(self, reaction):
        self.reactions.append(reaction)
        self.reaction_number += 1

    def first_reaction_inhibition(self, u, v):
        return self.REACTION(reactants=[u, v],
                             products=[self.additional_nodes[(u, v)]],
                             reversible=self.REVERSIBLE_REACTION)

    def second_reaction_inhibition(self, u, v):
        return self.REACTION([self.additional_nodes[(u, v)]],
                             [self.additional_nodes[v], u],
                             self.IRREVERSIBLE_REACTION)

    def first_reaction_activation(self, u, v):
        return self.REACTION(reactants=[u, self.additional_nodes[v]],
                             products=[self.additional_nodes[(u, v)]],
                             reversible=self.REVERSIBLE_REACTION)

    def second_reaction_activation(self, u, v):
        return self.REACTION(reactants=[self.additional_nodes[(u, v)]],
                             products=[u, v],
                             reversible=self.IRREVERSIBLE_REACTION)

    def add_backward_reaction(self, v):
        reaction = self.backward_reaction(v)
        self.backward_reactions.append(v)
        self.add_reaction(reaction)

    def backward_reaction(self, v):
        return self.REACTION(reactants=[v],
                             products=[self.additional_nodes[v]],
                             reversible=self.IRREVERSIBLE_REACTION)

    @staticmethod
    def human_readable_reaction(graph, reaction):
        """given Reaction (namedtuple) show it it human readable format"""
        reactants, products, reversible = reaction
        reactants = [ExpandGraph.node_name(graph, r) for r in reactants]
        products = [ExpandGraph.node_name(graph, p) for p in products]
        left_side = ExpandGraph.reaction_representation(reactants)
        right_side = ExpandGraph.reaction_representation(products)
        left_side = left_side.format(*reactants)
        right_side = right_side.format(*products)
        if reversible:
            return left_side + " <-> " + right_side
        return left_side + " -> " + right_side

    def human_readable_reactions(self):
        return [self.human_readable_reaction(self.graph, reaction) for reaction in self.reactions]

    def add_composite_nodes(self):
        next_node_number = max(self.graph.nodes())
        for edge in sorted(self.graph.edges()):
            next_node_number += 1
            if self.is_activation_edge(edge):
                self.graph.add_node(next_node_number,
                                    name='{} : {}'.format(*self.name_reactants(edge)))
            elif self.is_inhibition_edge(edge):
                self.graph.add_node(next_node_number,
                                    name='{} : not {}'.format(*self.name_reactants(edge)))
            else:
                raise ValueError("Edge weight can be either 0 or 1")
            self.additional_nodes[edge] = next_node_number

    def is_inhibition_edge(self, edge):
        return self.weight(edge) == self.INHIBITION

    def is_activation_edge(self, edge):
        return self.weight(edge) == self.ACTIVATION

    def name_reactants(self, reactants):
        return [self.node_name(self.graph, r) for r in reactants]

    def add_negation_of_nodes(self):
        next_node_number = max(self.graph.nodes())
        for node in sorted(self.graph.nodes()):
            if self.graph.in_degree(node) > 0:
                next_node_number += 1
                self.graph.add_node(next_node_number, name='not {}'.format(self.node_name(self.graph, node)))
                self.additional_nodes[node] = next_node_number

    def expand_graph(self):
        self.add_negation_of_nodes()
        self.add_composite_nodes()

    def cure_matrix_and_vector(self):
        """remove columns and rows that have all zeroes"""
        rows_to_delete = self._cure_matrix()
        self._cure_vector(rows_to_delete)
        self.deleted_rows_count = len(rows_to_delete)

    def _cure_vector(self, rows_to_delete):
        for i in reversed(rows_to_delete):
            del self.vector[i]

    def _cure_matrix(self):
        self._delete_zero_rows()
        self.matrix = list(zip(*self.matrix))
        rows_to_delete = self._delete_zero_rows()
        self.matrix = [list(row) for row in zip(*self.matrix)]
        return rows_to_delete

    def _delete_zero_rows(self):
        rows_to_delete = list()
        for i, row in enumerate(self.matrix):
            if all(element == 0 for element in row):
                rows_to_delete.append(i)
        for i in reversed(rows_to_delete):
            del self.matrix[i]
        return rows_to_delete

    @staticmethod
    def generate_empty_stoichiometric_matrix(number_of_rows, number_of_columns):
        return [[0 for _ in range(number_of_columns)] for _ in range(number_of_rows)]

    @staticmethod
    def reaction_representation(reagents, separator='+'):
        """
        Construct a reaction equation based on number of reagents

        Example with default separator of +:
        reaction_representation([1,2])
        '{} + {}'
        """
        assert isinstance(reagents, list)
        reagents_count = len(reagents)
        return "{}" + ("" if reagents_count == 1 else " {} {{}}".format(separator) * (reagents_count - 1))

    @staticmethod
    def node_name(graph, v):
        if 'name' in graph.node[v]:
            return nx.get_node_attributes(graph, 'name')[v]
        else:
            return "node %s has no name" % v

    def reconstruct_stoic_matrix_from_reactions(self):
        rows_count = self._number_of_reactants()
        columns_count = len(self.reactions)
        self.matrix = self.generate_empty_stoichiometric_matrix(rows_count, columns_count)
        self.vector = [0 for _ in range(columns_count)]
        for i, reaction in enumerate(self.reactions):
            left, right, reversible = reaction
            for e in left:
                self.matrix[e - 1][i] = self.REACTANT
            for e in right:
                self.matrix[e - 1][i] = self.PRODUCT
            if reversible:
                self.vector[i] = self.REVERSIBLE_REACTION
        self.cure_matrix_and_vector()

    def _number_of_reactants(self):
        l = [left + right for left, right, _ in self.reactions]
        l = list(itertools.chain.from_iterable(l))
        return max(l)
