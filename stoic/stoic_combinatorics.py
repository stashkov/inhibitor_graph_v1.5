from stoic.stoic_regular import ExpandGraph


class ExpandGraphCombinatorics(ExpandGraph):
    """
    Extend functionality by treating nodes > 1 in degree
    as simultaneous reactions, that happen at the same time,
    as opposed to being independent.

    Activation Edges:
        U -> N
        V -> N


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
        print()
        print()
        print(self.reactions, )

    def add_reactions_wo_combinatorics(self, node):
        """
        For nodes of in_degree = 1, just use methods from base class
        :type node: int
        """
        edge = next(self.graph.in_edges_iter(node))  # this always returns a single edge
        super().add_activation_reactions(edge)
        super().add_inhibition_reactions(edge)

    def add_reactions_w_combinatorics(self, node):
        """We have 2 options for all activation edges"""
        self.all_activation_edges_complex_reactions(node)

    def all_activation_edges_separate_reactions(self, node):
        """
        Activation Edges:
            U -> N
            V -> N
        Separate:
            U + not(N) <-> U:N -> U + N
            V + not(N) <-> V:N -> V + N
            N -> not(N)
        Note:
             If you have more incoming nodes, add another equation
        """
        pass

    def all_activation_edges_complex_reactions(self, node):
        """
        Activation Edges:
            U -> N
            V -> N

        Complex:
                U + V + not(N) <-> U:V:N -> U + V + N
                N -> not(N)
        Note:
            If you have more incoming nodes, add another reactant to first equation
        """
        self.add_reaction(self.first_reaction_all_activation_option_one(node))
        self.add_reaction(self.second_reaction_all_activation_option_one(node))
        if node not in self.backward_reactions:
            self.add_backward_reaction(node)

    def first_reaction_all_activation_option_one(self, node):
        return self.REACTION(reactants=self.extract_reactants(node),
                             products=[(self.additional_nodes[self.composite_node(node)])],
                             reversible=self.REVERSIBLE_REACTION)

    def second_reaction_all_activation_option_one(self, node):
        return self.REACTION(reactants=[(self.additional_nodes[self.composite_node(node)])],
                             products=(self.extract_composite_reactant(node)),
                             reversible=self.IRREVERSIBLE_REACTION)

    def add_composite_nodes(self):
        next_node_number = max(self.graph.nodes())
        for node, in_degree in list(self.graph.in_degree_iter()):
            next_node_number += 1
            if in_degree > 1:
                self.add_to_graph(node, next_node_number)
                self.additional_nodes[self.composite_node(node)] = next_node_number
        super(ExpandGraphCombinatorics, self).add_composite_nodes()

    def composite_node(self, node):
        """
        :type node: int
        """
        return tuple(self.extract_composite_reactant(node))

    def add_to_graph(self, node, next_node_number):
        name = self.placeholder(node)
        reactants = self.get_reactants(node)
        self.graph.add_node(next_node_number, name=name.format(*reactants))

    def get_reactants(self, node):
        return self.name_reactants(self.composite_node(node))

    def extract_reactants(self, node):
        """
        Given a node, returns incoming nodes + negation of a given node

        Example: given 3 (with 1 and 2 going to 3), returns [1,2,not(3)]
        :type node: int
        """
        regular_reactants = [u for u, _ in self.graph.in_edges(node)]
        phosporilated_node = [self.additional_nodes[node]]
        return sorted(regular_reactants + phosporilated_node)

    def extract_composite_reactant(self, node):
        """
        Given a node, returns incoming nodes + negation of a given node

        Example: given 3 (with 1 and 2 going to 3), returns [1,2,3]
        :type node: int
        """
        return sorted([u for u, _ in self.graph.in_edges(node)] + [node])

    def placeholder(self, node):
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
