import networkx as nx


class Combinatorics:
    ACTIVATION = 0
    INHIBITION = 1

    def __init__(self, graph):
        assert isinstance(graph, nx.DiGraph)
        self.graph = graph
        self.cur_node = max(self.graph.nodes())
        self.node_helpers = dict()
        self.setup()

    def setup(self):
        self.negate_nodes()

    def negate_nodes(self):
        """
        each node U gets node "not U" in the graph
        """
        extra_nodes = list()
        for node, d in self.graph.nodes(data=True):
            if self.graph.in_degree(node) > 0:
                self.cur_node += 1
                self.node_helpers[node] = self.cur_node
                extra_nodes.append((self.cur_node, ('not ' + d['name'])))
        for node, name in extra_nodes:
            self.graph.add_node(node, name=name)

    def _prepare_node(self, left, right):
        """
        Prepares a composite enzyme which can be referred to later
        as a tuple of its individual parts.

        Left and right side can be different or the same.
        Example 1: U+V+Z+notN -> U:V:Z:N
        Example 2: U+N -> U:N
        :type right: list
        :type left: list
        :param left: side of the equation
        :param right: side of the equation
        :return:
        """
        self.cur_node += 1
        self.node_helpers[tuple(left)] = (self.cur_node,)
        self._add_node(nodes=right)

    def activated_separate(self):
        """
        Equations 3.4 from thesis
        :return:
        """
        for u, v, d in self.graph.edges(data=True):
            if self._is_all_incoming_edges_are_activation_edges(v):
                left = [u, self.node_helpers[v]]
                right = [u, v]
                self._prepare_node(left, right)

    def activated_combination(self):
        """
        Equations 3.3 from thesis
        :return:
        """
        for node in self.graph.nodes():
            if self._is_all_incoming_edges_are_activation_edges(node):
                left = self.graph.predecessors(node) + [self.node_helpers[node]]
                right = self.graph.predecessors(node) + [node]
                self._prepare_node(left, right)

    def inhibited(self):
        """
        Equations 3.2 from thesis
        """
        for node in self.graph.nodes():
            if self._is_all_incoming_edges_are_inhibition_edges(node):
                left = self.graph.predecessors(node) + [node]
                self._prepare_node(left, left)

    def mixed(self):
        """
        Equations 3.1 from thesis
        :return:
        """
        for u, v, d in self.graph.edges(data=True):
            if self._is_all_incoming_edges_are_mixed(v):
                left = [u, v]
                self._prepare_node(left, left)

    @staticmethod
    def _template(composite_enzyme):
        return '{}' + ':{}' * (len(composite_enzyme) - 1)

    def _is_all_incoming_edges_are_activation_edges(self, node):
        if self.graph.in_degree(node) > 1:
            return all([self.graph.edge[p][node]['weight'] == self.ACTIVATION for p in self.graph.predecessors(node)])
        else:
            return False

    def _is_all_incoming_edges_are_inhibition_edges(self, node):
        if self.graph.in_degree(node) > 1:
            return all([self.graph.edge[p][node]['weight'] == self.INHIBITION for p in self.graph.predecessors(node)])
        else:
            return False

    def _is_all_incoming_edges_are_mixed(self, node):
        if self.graph.in_degree(node) > 1:
            return not self._is_all_incoming_edges_are_activation_edges(node) and \
                   not self._is_all_incoming_edges_are_inhibition_edges(node)
        else:
            return False

    def _add_node(self, nodes):
        template = self._template(nodes)
        self.graph.add_node(self.cur_node, name=template.format(*self._node_name(nodes)))

    def _node_name(self, nodes):
        if isinstance(nodes, int):
            return self.graph.node[nodes]['name']
        if isinstance(nodes, list):
            return [self.graph.node[node]['name'] for node in nodes]
