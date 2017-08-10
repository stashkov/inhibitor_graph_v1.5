import networkx as nx


class ExpandGraph(object):
    def __init__(self, graph):
        assert isinstance(graph, nx.DiGraph)
        assert all('weight' in d.keys() for u, v, d in graph.edges(data=True)), \
            "all edges must have weights"
        self.graph, self.additional_nodes = ExpandGraph.expand_graph(graph)
        self.backward_reactions = list()  # track reactions
        self.matrix = list()
        self.vector = list()
        self.initialize_matrix_and_vector()
        self.fill_in_stoichiometric_matrix()

    @property
    def reactant(self):
        """
        terms that are on the left in chemical equation
        in stoichiometric matrices denoted by -1
        """
        return -1

    @property
    def product(self):
        """
        terms that are on the right in chemical equation
        in stoichiometric matrices denoted by 1
        """
        return 1

    def initialize_matrix_and_vector(self):
        """
        As per article,
            each activation gives us 2 * n + 1 reactions ( where n is # of edges)
            each inhibition gives us 2 reactions
        """
        rows = len(self.graph.nodes())
        inhibition_constant = 2
        n_of_activation_edges = sum(1 for _, _, d in self.graph.edges(data=True) if d['weight'] == 0)
        n_of_activation_reactions = 2 * n_of_activation_edges + 1 if n_of_activation_edges != 0 else 0
        n_of_inhibition_reactions = \
            inhibition_constant * sum(1 for _, _, d in self.graph.edges(data=True) if d['weight'] == 1)
        columns = n_of_activation_reactions + n_of_inhibition_reactions
        self.matrix = self.generate_empty_stoichiometric_matrix(rows, columns)
        self.vector = [0 for _ in range(columns)]

    def fill_in_stoichiometric_matrix(self):
        reaction_number = 0
        for edge in self.graph.edges():
            if self.graph.get_edge_data(*edge)['weight'] == 0:
                reaction_number = self.add_activation_edge_reactions(edge, reaction_number)
            if self.graph.get_edge_data(*edge)['weight'] == 1:
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
        reversible_reaction = 1
        assert isinstance(edge, tuple)
        u, v = edge
        self.add_first_activation_reaction(u, v, reaction_number)
        self.vector[reaction_number] = reversible_reaction
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
        reversible_reaction = 1
        assert isinstance(edge, tuple)
        u, v = edge
        self.add_first_inhibition_reaction(u, v, reaction_number)
        self.vector[reaction_number] = reversible_reaction
        reaction_number += 1
        self.add_second_inhibition_reaction(u, v, reaction_number)
        reaction_number += 1
        return reaction_number

    def add_first_inhibition_reaction(self, u, v, column):
        # print("First Reaction: {} + {} <-> {}".format(u, v, self.additional_nodes[(u, v)]))
        self.matrix[u - 1][column] = self.reactant
        self.matrix[v - 1][column] = self.reactant
        self.matrix[self.additional_nodes[(u, v)] - 1][column] = self.product

    def add_second_inhibition_reaction(self, u, v, column):
        # print("Second Reaction: {} -> {} + {}".format(self.additional_nodes[(u, v)], u, self.additional_nodes[v]))
        self.matrix[self.additional_nodes[(u, v)] - 1][column] = self.reactant
        self.matrix[u - 1][column] = self.product
        self.matrix[self.additional_nodes[v] - 1][column] = self.product

    def add_first_activation_reaction(self, u, v, column):
        # print("First Reaction: {} + {} <-> {}".format(u, self.additional_nodes[v], self.additional_nodes[(u, v)]))
        self.matrix[u - 1][column] = self.reactant
        self.matrix[self.additional_nodes[v] - 1][column] = self.reactant
        self.matrix[self.additional_nodes[(u, v)] - 1][column] = self.product

    def add_second_activation_reaction(self, u, v, column):
        # print("Second Reaction: {} -> {} + {}".format(self.additional_nodes[(u, v)], u, v))
        self.matrix[self.additional_nodes[(u, v)] - 1][column] = self.reactant
        self.matrix[u - 1][column] = self.product
        self.matrix[v - 1][column] = self.product

    def add_third_activation_reaction(self, v, column):
        # print("Third Reaction: {} -> {}".format(v, self.additional_nodes[v]))
        self.matrix[v - 1][column] = self.reactant
        self.matrix[self.additional_nodes[v] - 1][column] = self.product
        self.backward_reactions.append(v)

    @staticmethod
    def generate_empty_stoichiometric_matrix(number_of_rows, number_of_columns):
        return [[0 for _ in range(number_of_columns)] for _ in range(number_of_rows)]

    @staticmethod
    def add_composite_nodes(additional_nodes, graph):
        assert all('weight' in d.keys() for _, _, d in graph.edges(data=True)), \
            "all edges must have weights"
        next_node_number = max(graph.nodes())
        for edge in graph.edges():
            next_node_number += 1
            u, v = edge
            if graph.get_edge_data(*edge)['weight'] == 0:
                graph.add_node(next_node_number, label='Negation of {} and {}'.format(u, v))
            if graph.get_edge_data(*edge)['weight'] == 1:
                graph.add_node(next_node_number, label='Negation of {} and not {}'.format(u, v))
            additional_nodes[edge] = next_node_number
        return graph, additional_nodes

    @staticmethod
    def add_negation_of_nodes(additional_nodes, graph):
        next_node_number = max(graph.nodes())
        for node in graph.nodes():
            if graph.in_degree(node) > 0:
                next_node_number += 1
                graph.add_node(next_node_number, label='Negation of ' + str(node))
                additional_nodes[node] = next_node_number
        return graph, additional_nodes

    @staticmethod
    def expand_graph(graph):
        assert all('weight' in d.keys() for u, v, d in graph.edges(data=True)), \
            "all edges must have weights"
        additional_nodes = dict()
        graph, additional_nodes = ExpandGraph.add_negation_of_nodes(additional_nodes, graph)
        graph, additional_nodes = ExpandGraph.add_composite_nodes(additional_nodes, graph)
        return graph, additional_nodes