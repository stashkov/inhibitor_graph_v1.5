from collections import namedtuple

import networkx as nx


class ExpandGraph(object):
    INHIBITION = 1  # edges in a graph that have weight 1 are considered inhibition edges
    ACTIVATION = 0  # edges in a graph that have weight 1 are considered activation edges
    REACTANT = -1  # terms that are on the left in chemical equation in stoichiometric matrices denoted by -1
    PRODUCT = 1  # terms that are on the right in chemical equation in stoichiometric matrices denoted by -1
    REVERSIBLE_REACTION = 1  # reaction that is reversible in reversibility vector (otherwise its 0)
    REACTION = namedtuple('Reaction', 'reactants, products')

    def __init__(self, graph):
        assert isinstance(graph, nx.DiGraph)
        assert all('weight' in d.keys() for _, _, d in graph.edges(data=True)), \
            "all edges must have weights"
        self.graph = graph
        self.additional_nodes = self.expand_graph()

        self.backward_reactions = list()  # track reactions
        self.matrix, self.vector = self.initialize_matrix_and_vector()
        self.reactions = list()  # TODO add add_to_reaction_list(reaction) with assert for tuple content
        self.deleted_rows_count = 0
        self.reaction_number = 0

        self.fill_in_stoichiometric_matrix()
        self.cure_matrix_and_vector()

    def initialize_matrix_and_vector(self):
        """
        As per article,
            ??? each activation gives us 2 * n + 1 reactions ( where n is # of edges)
            ??? each inhibition gives us 2 reactions
        """
        rows = len(self.graph.nodes())
        columns = len(list(self.graph.edges())) * 2 + len(list(self.graph.nodes()))
        self.matrix = self.generate_empty_stoichiometric_matrix(rows, columns)
        self.vector = [0 for _ in range(columns)]
        return self.matrix, self.vector

    def fill_in_stoichiometric_matrix(self):
        for i, edge in enumerate(sorted(self.graph.edges())):
            self.add_activation_reaction_to_stoic_matrix(edge)
            self.add_inhibition_reaction_to_stoic_matrix(edge)

    def add_inhibition_reaction_to_stoic_matrix(self, edge):
        if self.weight(edge) == self.INHIBITION:
            self.add_inhibition_edge_reactions(edge)

    def weight(self, edge):
        return self.graph.get_edge_data(*edge)['weight']

    def add_activation_reaction_to_stoic_matrix(self, edge):
        if self.weight(edge) == self.ACTIVATION:
            self.add_activation_edge_reactions(edge)

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
        self.add_first_activation_reaction(u, v)
        self.add_second_activation_reaction(u, v)
        if v not in self.backward_reactions:
            self.add_third_activation_reaction(v)

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
        self.add_first_inhibition_reaction(u, v)
        self.add_second_inhibition_reaction(u, v)

    def add_first_inhibition_reaction(self, u, v):
        reaction = self.REACTION([u, v], [self.additional_nodes[(u, v)]])
        self.reactions.append(reaction)
        self.matrix[u - 1][self.reaction_number] = self.REACTANT
        self.matrix[v - 1][self.reaction_number] = self.REACTANT
        self.matrix[self.additional_nodes[(u, v)] - 1][self.reaction_number] = self.PRODUCT
        self.vector[self.reaction_number] = self.REVERSIBLE_REACTION
        self.reaction_number += 1

    def add_second_inhibition_reaction(self, u, v):
        reaction = self.REACTION([self.additional_nodes[(u, v)], u], [self.additional_nodes[v]])
        self.reactions.append(reaction)
        self.matrix[self.additional_nodes[(u, v)] - 1][self.reaction_number] = self.REACTANT
        self.matrix[u - 1][self.reaction_number] = self.PRODUCT
        self.matrix[self.additional_nodes[v] - 1][self.reaction_number] = self.PRODUCT
        self.reaction_number += 1

    def add_first_activation_reaction(self, u, v):
        reaction = self.REACTION([u, self.additional_nodes[v]], [self.additional_nodes[(u, v)]])
        self.reactions.append(reaction)
        self.matrix[u - 1][self.reaction_number] = self.REACTANT
        self.matrix[self.additional_nodes[v] - 1][self.reaction_number] = self.REACTANT
        self.matrix[self.additional_nodes[(u, v)] - 1][self.reaction_number] = self.PRODUCT
        self.vector[self.reaction_number] = self.REVERSIBLE_REACTION
        self.reaction_number += 1

    def add_second_activation_reaction(self, u, v):
        reaction = self.REACTION([self.additional_nodes[(u, v)]], [u, v])
        self.reactions.append(reaction)
        self.matrix[self.additional_nodes[(u, v)] - 1][self.reaction_number] = self.REACTANT
        self.matrix[u - 1][self.reaction_number] = self.PRODUCT
        self.matrix[v - 1][self.reaction_number] = self.PRODUCT
        self.reaction_number += 1

    def add_third_activation_reaction(self, v):
        reaction = self.REACTION([v], [self.additional_nodes[v]])
        self.reactions.append(reaction)
        self.matrix[v - 1][self.reaction_number] = self.REACTANT
        self.matrix[self.additional_nodes[v] - 1][self.reaction_number] = self.PRODUCT
        self.backward_reactions.append(v)
        self.reaction_number += 1

    @staticmethod
    def human_readable_reaction(graph, reaction):
        """given Reaction (namedtuple) show it it human readable format"""
        reactants, products = reaction
        reactants = [ExpandGraph.node_name(graph, r) for r in reactants]
        products = [ExpandGraph.node_name(graph, p) for p in products]
        # TODO add reversibility of the reaction to namedtuple
        left_side = ExpandGraph.reaction_representation(reactants)
        right_side = ExpandGraph.reaction_representation(products)
        left_side = left_side.format(*reactants)
        right_side = right_side.format(*products)
        return left_side + " -> " + right_side

    def human_readable_reactions(self):
        return [self.human_readable_reaction(self.graph, reaction) for reaction in self.reactions]

    def add_composite_nodes(self, additional_nodes):
        next_node_number = max(self.graph.nodes())
        for edge in sorted(self.graph.edges()):
            next_node_number += 1
            u, v = edge
            edge_weight = self.weight(edge)
            if edge_weight == self.ACTIVATION:
                self.graph.add_node(next_node_number,
                                    name='{} : {}'.format(self.node_name(self.graph, u),
                                                          self.node_name(self.graph, v)))
            elif edge_weight == self.INHIBITION:
                self.graph.add_node(next_node_number,
                                    name='{} : not {}'.format(self.node_name(self.graph, u),
                                                              self.node_name(self.graph, v)))
            else:
                raise ValueError("Edge weight can be either 0 or 1")
            additional_nodes[edge] = next_node_number
        return additional_nodes

    def add_negation_of_nodes(self, additional_nodes):
        next_node_number = max(self.graph.nodes())
        for node in sorted(self.graph.nodes()):
            if self.graph.in_degree(node) > 0:
                next_node_number += 1
                self.graph.add_node(next_node_number, name='not {}'.format(self.node_name(self.graph, node)))
                additional_nodes[node] = next_node_number
        return additional_nodes

    def expand_graph(self):
        additional_nodes = dict()
        additional_nodes = self.add_negation_of_nodes(additional_nodes)
        additional_nodes = self.add_composite_nodes(additional_nodes)
        return additional_nodes

    def cure_matrix_and_vector(self):
        self._delete_zero_rows()
        self.matrix = list(zip(*self.matrix))
        rows_to_delete = self._delete_zero_rows()
        self.matrix = [list(row) for row in zip(*self.matrix)]

        # cure vector
        for i in reversed(rows_to_delete):
            del self.vector[i]
        self.deleted_rows_count = len(rows_to_delete)

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
        pass
