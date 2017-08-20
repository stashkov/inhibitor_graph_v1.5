import networkx as nx
from collections import namedtuple


class ExpandGraph(object):
    INHIBITION = 1  # edges in a graph that have weight 1 are considered inhibition edges
    ACTIVATION = 0  # edges in a graph that have weight 1 are considered activation edges
    REACTANT = -1  # terms that are on the left in chemical equation in stoichiometric matrices denoted by -1
    PRODUCT = 1  # terms that are on the right in chemical equation in stoichiometric matrices denoted by -1
    REVERSIBLE_REACTION = 1  # reaction that is reversible in reversibility vector (otherwise its 0)
    Reaction = namedtuple('Reaction', 'reactants, products')

    def __init__(self, graph):
        assert isinstance(graph, nx.DiGraph)
        assert all('weight' in d.keys() for _, _, d in graph.edges(data=True)), \
            "all edges must have weights"
        self.graph = graph
        self.graph, self.additional_nodes = self.expand_graph(graph)
        self.backward_reactions = list()  # track reactions
        self.matrix, self.vector = self.initialize_matrix_and_vector()
        self.reactions = list()
        self.reactants = list()
        self.deleted_rows_count = 0

        self.fill_in_stoichiometric_matrix()
        self.cure_matrix_and_vector()

    def initialize_matrix_and_vector(self):
        """
        As per article,
            each activation gives us 2 * n + 1 reactions ( where n is # of edges)
            each inhibition gives us 2 reactions
        """
        rows = len(self.graph.nodes())
        columns = len(list(self.graph.edges())) * 2 + len(list(self.graph.nodes()))
        self.matrix = self.generate_empty_stoichiometric_matrix(rows, columns)
        self.vector = [0 for _ in range(columns)]
        return self.matrix, self.vector

    def fill_in_stoichiometric_matrix(self):
        reaction_number = 0
        # TODO remove sorted, if Sampler does not provide ordered number of EFMs
        for i, edge in enumerate(sorted(self.graph.edges())):
            if self.graph.get_edge_data(*edge)['weight'] == self.ACTIVATION:
                reaction_number = self.add_activation_edge_reactions(edge, reaction_number)
            if self.graph.get_edge_data(*edge)['weight'] == self.INHIBITION:
                reaction_number = self.add_inhibition_edge_reactions(edge, reaction_number)

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
        self.add_first_activation_reaction(u, v, reaction_number)
        reaction_number += 1
        self.add_second_activation_reaction(u, v, reaction_number)
        reaction_number += 1
        if v not in self.backward_reactions:
            self.add_third_activation_reaction(v, reaction_number)
            reaction_number += 1
        return reaction_number

    def add_inhibition_edge_reactions(self, edge, reaction_number):
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
        self.add_first_inhibition_reaction(u, v, reaction_number)
        reaction_number += 1
        self.add_second_inhibition_reaction(u, v, reaction_number)
        reaction_number += 1
        return reaction_number

    def add_first_inhibition_reaction(self, u, v, column):
        reaction = self.Reaction([u, v], [self.additional_nodes[(u, v)]])
        self.reactions.append(reaction)
        self.matrix[u - 1][column] = self.REACTANT
        self.matrix[v - 1][column] = self.REACTANT
        self.matrix[self.additional_nodes[(u, v)] - 1][column] = self.PRODUCT
        self.vector[column] = self.REVERSIBLE_REACTION

    def add_second_inhibition_reaction(self, u, v, column):
        reaction = self.Reaction([self.additional_nodes[(u, v)], u], [self.additional_nodes[v]])
        self.reactions.append(reaction)
        self.matrix[self.additional_nodes[(u, v)] - 1][column] = self.REACTANT
        self.matrix[u - 1][column] = self.PRODUCT
        self.matrix[self.additional_nodes[v] - 1][column] = self.PRODUCT

    def add_first_activation_reaction(self, u, v, column):
        reaction = self.Reaction([u, self.additional_nodes[v]], [self.additional_nodes[(u, v)]])
        self.reactions.append(reaction)
        self.matrix[u - 1][column] = self.REACTANT
        self.matrix[self.additional_nodes[v] - 1][column] = self.REACTANT
        self.matrix[self.additional_nodes[(u, v)] - 1][column] = self.PRODUCT
        self.vector[column] = self.REVERSIBLE_REACTION

    def add_second_activation_reaction(self, u, v, column):
        reaction = self.Reaction([self.additional_nodes[(u, v)]], [u, v])
        self.reactions.append(reaction)
        self.matrix[self.additional_nodes[(u, v)] - 1][column] = self.REACTANT
        self.matrix[u - 1][column] = self.PRODUCT
        self.matrix[v - 1][column] = self.PRODUCT

    def add_third_activation_reaction(self, v, column):
        reaction = self.Reaction([v], [self.additional_nodes[v]])
        self.reactions.append(reaction)
        self.matrix[v - 1][column] = self.REACTANT
        self.matrix[self.additional_nodes[v] - 1][column] = self.PRODUCT
        self.backward_reactions.append(v)

    def node_name(self, v):
        # assert all('name' in d.keys() for _, d in self.graph.nodes(data=True)), \
        #     "all nodes must have name"
        if 'name' in self.graph.nodes(v)[0][1]:
            return nx.get_node_attributes(self.graph, 'name')[v]
        else:
            return "node %s has no name" % v

    def human_readable_reaction(self, reaction):
        """given Reaction (namedtuple) show it it human readable format"""
        reactants, products = reaction
        reactants = [self.node_name(r) for r in reactants]
        products = [self.node_name(p) for p in products]
        # TODO add reversibility of the reaction to namedtuple
        left_side = self.reaction_representation(reactants)
        right_side = self.reaction_representation(products)
        left_side = left_side.format(*reactants)
        right_side = right_side.format(*products)
        return left_side + " -> " + right_side

    @staticmethod
    def reaction_representation(reagents):
        """
        Dynamically construct a reaction equation based on number of reagent

        Example:
        >>> reaction_representation([1,2])
        '{} + {}'
        """
        assert isinstance(reagents, list)
        reagents_count = len(reagents)
        return "{}" + ("" if reagents_count == 1 else " + {}" * (reagents_count - 1))

    @staticmethod
    def generate_empty_stoichiometric_matrix(number_of_rows, number_of_columns):
        return [[0 for _ in range(number_of_columns)] for _ in range(number_of_rows)]

    def add_composite_nodes(self, additional_nodes, graph):
        assert all('weight' in d.keys() for _, _, d in graph.edges(data=True)), \
            "all edges must have weights"
        next_node_number = max(graph.nodes())
        # TODO remove sorted, if Sampler does not provide ordered number of EFMs
        for edge in sorted(graph.edges()):
            next_node_number += 1
            u, v = edge
            if graph.get_edge_data(*edge)['weight'] == self.ACTIVATION:
                graph.add_node(next_node_number, name='{} : {}'.format(self.node_name(u), self.node_name(v)))
            if graph.get_edge_data(*edge)['weight'] == self.INHIBITION:
                graph.add_node(next_node_number, name='{} : not {}'.format(self.node_name(u), self.node_name(v)))
            additional_nodes[edge] = next_node_number
        return graph, additional_nodes

    def add_negation_of_nodes(self, additional_nodes, graph):
        next_node_number = max(graph.nodes())
        # TODO remove sorted, if Sampler does not provide ordered number of EFMs
        for node in sorted(graph.nodes()):
            if graph.in_degree(node) > 0:
                next_node_number += 1
                graph.add_node(next_node_number, name='not ' + self.node_name(node))
                additional_nodes[node] = next_node_number
        return graph, additional_nodes

    def expand_graph(self, graph):
        assert all('weight' in d.keys() for u, v, d in graph.edges(data=True)), \
            "all edges must have weights"
        additional_nodes = dict()
        graph, additional_nodes = self.add_negation_of_nodes(additional_nodes, graph)
        graph, additional_nodes = self.add_composite_nodes(additional_nodes, graph)
        return graph, additional_nodes

    def cure_matrix_and_vector(self):
        m = list(zip(*self.matrix))
        rows_to_delete = list()
        for i, row in enumerate(m):
            if all(element == 0 for element in row):
                rows_to_delete.append(i)
        for i in reversed(rows_to_delete):
            del m[i]
        # cure vector
        for i in reversed(rows_to_delete):
            del self.vector[i]

        self.matrix = [list(row) for row in zip(*m)]
        self.deleted_rows_count = len(rows_to_delete)
