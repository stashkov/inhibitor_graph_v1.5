from stoic.generate_stoic import ExpandGraph
import itertools


class ExpandGraphCombinatorics(ExpandGraph):
    def fill_in_stoichiometric_matrix(self):
        for node, in_degree in self.graph.in_degree_iter():
            if in_degree == 1:
                self.add_reactions_wo_combinatorics(node)
            elif in_degree > 1:
                self.add_reactions_w_combinatorics(node)

    def add_reactions_wo_combinatorics(self, node):
        edge = next(self.graph.in_edges_iter(node))  # this always returns a single edge
        super().add_activation_reaction_to_stoic_matrix(edge)
        super().add_inhibition_reaction_to_stoic_matrix(edge)

    def add_reactions_w_combinatorics(self, node):
        """
        Given a node which has in degree > 1,
        """
        self.add_first_activation_reaction_combinatorics(node)
        self.add_second_activation_reaction_combinatorics(node)
        if node not in self.backward_reactions:
            self.add_third_activation_reaction(node)

    def add_first_activation_reaction_combinatorics(self, node):
        left_hand = self.extract_reactants(node)
        right_hand = self.additional_nodes[self.composite_node(node)]
        reaction = self.Reaction(left_hand, [right_hand])
        self.reactions.append(reaction)
        for i in left_hand:
            self.matrix[i - 1][self.reaction_number] = self.REACTANT
        self.matrix[right_hand - 1][self.reaction_number] = self.PRODUCT
        self.vector[self.reaction_number] = self.REVERSIBLE_REACTION
        self.reaction_number += 1

    def add_second_activation_reaction_combinatorics(self, node):
        left_hand = self.extract_reactants(node)
        right_hand = self.additional_nodes[self.composite_node(node)]
        reaction = self.Reaction([right_hand], left_hand)
        self.reactions.append(reaction)
        for i in left_hand:
            self.matrix[i - 1][self.reaction_number] = self.PRODUCT
        self.matrix[right_hand - 1][self.reaction_number] = self.REACTANT
        self.reaction_number += 1

    def add_composite_nodes(self, additional_nodes):
        next_node_number = max(self.graph.nodes())
        for node, in_degree in list(self.graph.in_degree_iter()):
            next_node_number += 1
            if in_degree > 1:
                name, reactants = self.generate_combinatorics_node(node)
                self.graph.add_node(next_node_number, name=name.format(*reactants))
                additional_nodes[self.composite_node(node)] = next_node_number
        super(ExpandGraphCombinatorics, self).add_composite_nodes(additional_nodes)
        return additional_nodes

    def composite_node(self, node):
        return tuple(self.extract_reactants(node))

    def generate_combinatorics_node(self, node):
        name = self.generate_name_str(node)
        reactants = self.generate_reactants(node)
        return name, reactants

    def generate_reactants(self, node):
        reactants = self.extract_reactants(node)
        reactants = self.name_reactants(reactants)
        return reactants

    def name_reactants(self, reactants):
        return [self.node_name(self.graph, r) for r in reactants]

    def extract_reactants(self, node):
        """
        from list of tuples (edges) extract unique reactants
        :type node: int
        """
        edges = self.graph.in_edges(node)
        return sorted(list(set(list(itertools.chain(*edges)))))

    def generate_name_str(self, node):
        """
        returns a string of "{}:{}:{}" based on the number of incoming nodes
        :type edges: list
        :param edges:
        :return:
        """
        edges = self.graph.in_edges(node)
        name = self.reaction_representation([u for u, _ in edges], separator=':')
        name += ": not {}"
        return name

    @staticmethod
    def assert_edges(edges):
        assert isinstance(edges, list)
        assert all(isinstance(edge, tuple) for edge in edges)
