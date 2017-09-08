from stoic.stoic_regular import ExpandGraph


class ExpandGraphCombinatorics(ExpandGraph):
    """
    Extend functionality by treating nodes > 1 in degree
    as simultaneous reactions, that happen at the same time,
    as opposed to being independent.

    Activation Edges:
        U -> N
        V -> N

    Option 2:
        U + V + not(N) <-> U:V:N -> U + V + N
        N -> not(N)
    Note:
        If you have more incoming nodes, add another reactant to first equation

    Inhibition Edges:
        U -| N
        V -> N

    Option 1:
        U + N <-> U:N -> U + not(N)
        V + N <-> V:N -> V + not(N)
        N -> not(N)
    Note:
        If you have more incoming edges, add another equation

    Option 2:
        U + V + N <-> U:V:N -> U + V + not(N)
    Note:
        Was decided to skip this
    """
    def add_reactions(self):
        for node, in_degree in self.graph.in_degree_iter():
            if in_degree == 1:
                self.add_reactions_wo_combinatorics(node)
            elif in_degree > 1:
                self.add_reactions_w_combinatorics(node)

    def add_reactions_wo_combinatorics(self, node):
        """
        For nodes of in_degree = 1, just use methods from base class
        :type node: int
        """
        edge = next(self.graph.in_edges_iter(node))  # this always returns a single edge
        super().add_activation_reactions(edge)
        super().add_inhibition_reactions(edge)

    def add_reactions_w_combinatorics(self, node):
        """
        Activation Edges:
            U -> N
            V -> N
        Option 1:
            U + not(N) <-> U:N -> U + N
            V + not(N) <-> V:N -> V + N
            N -> not(N)
        Note:
             If you have more incoming nodes, add another equation
        :param node:
        :return:
        """
        self.add_first_activation_reaction_combinatorics(node)
        self.add_second_activation_reaction_combinatorics(node)
        if node not in self.backward_reactions:
            self.add_third_activation_reaction(node)

    def add_first_activation_reaction_combinatorics(self, node):
        reaction = self.REACTION(reactants=self.extract_reactants(node),
                                 products=[(self.additional_nodes[self.composite_node(node)])],
                                 reversible=self.REVERSIBLE_REACTION)

        self.reactions.append(reaction)
        self.reaction_number += 1

    def add_second_activation_reaction_combinatorics(self, node):
        reaction = self.REACTION(reactants=[(self.additional_nodes[self.composite_node(node)])],
                                 products=(self.extract_reactants_all_active(node)),
                                 reversible=self.IRREVERSIBLE_REACTION)
        a = self.human_readable_reaction(self.graph, reaction)
        self.reactions.append(reaction)
        self.reaction_number += 1

    def add_composite_nodes(self):
        next_node_number = max(self.graph.nodes())
        for node, in_degree in list(self.graph.in_degree_iter()):
            next_node_number += 1
            if in_degree > 1:
                name, reactants = self.generate_combinatorics_node(node)
                self.graph.add_node(next_node_number, name=name.format(*reactants))
                self.additional_nodes[self.composite_node(node)] = next_node_number
        super(ExpandGraphCombinatorics, self).add_composite_nodes()

    def composite_node(self, node):
        """
        :type node: int
        :param node:
        :return:
        """
        return tuple(self.extract_reactants_all_active(node))

    def generate_combinatorics_node(self, node):
        name = self.generate_name_str(node)
        reactants = self.generate_reactants(node)
        return name, reactants

    def generate_reactants(self, node):
        reactants = self.composite_node(node)
        reactants = self.name_reactants(reactants)
        return reactants

    def name_reactants(self, reactants):
        return [self.node_name(self.graph, r) for r in reactants]

    def extract_reactants(self, node):
        """
        Given a node, returns incoming nodes + negation of a given node

        Example: given 3 (with 1 and 2 going to 3), returns [1,2,not(3)]
        :type node: int
        """
        regular_reactants = [u for u, _ in self.graph.in_edges(node)]
        phosporilated_node = [self.additional_nodes[node]]
        return sorted(regular_reactants + phosporilated_node)

    def extract_reactants_all_active(self, node):
        """
        Given a node, returns incoming nodes + negation of a given node

        Example: given 3 (with 1 and 2 going to 3), returns [1,2,3]
        :type node: int
        """
        return sorted([u for u, _ in self.graph.in_edges(node)] + [node])



    def generate_name_str(self, node):
        """
        returns a string of "{}:{}:{}" based on the number of incoming nodes
        :type node: int
        :return:
        """
        edges = self.graph.in_edges(node)
        name = self.reaction_representation([u for u, _ in edges] + [node], separator=':')
        return name

    @staticmethod
    def assert_edges(edges):
        assert isinstance(edges, list)
        assert all(isinstance(edge, tuple) for edge in edges)
