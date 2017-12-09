import networkx as nx


class Combinatorics:
    ACTIVATION = 0
    INHIBITION = 1

    def __init__(self, graph):
        assert isinstance(graph, nx.DiGraph)
        self.graph = graph
        self.cur_node = max(self.graph.nodes())
        self.node_helpers = dict()

    def setup_graph(self):
        self.negate_nodes()
        self.composite_mix_activation()

    def node_name(self, nodes):
        if isinstance(nodes, int):
            return self.graph.node[nodes]['name']
        if isinstance(nodes, list):
            return [self.graph.node[node]['name'] for node in nodes]

    def negate_nodes(self):
        """
        each node U gets node "not U" in the graph
        """
        for node, d in self.graph.nodes(data=True):
            self.cur_node += 1
            self.graph.add_node(self.cur_node, name=('not ' + d['name']))
            self.node_helpers[node] = self.cur_node

    # TODO remove this func?
    def composite_mix_activation(self):
        """
        Equations 3.1 from thesis
        each edge U->V gets node "U:V" in the graph
        """
        self.negate_nodes()
        for u, v, d in self.graph.edges(data=True):
            self.cur_node += 1
            self.node_helpers[(u, v)] = (self.cur_node,)
            if d['weight'] == self.ACTIVATION:
                self._add_node([u, v], template='{}:{}')
            elif d['weight'] == self.INHIBITION:
                self._add_node(nodes=[u, self.node_helpers[v]], template='{}:{}')

    def _add_node(self, nodes, template):
        self.graph.add_node(self.cur_node, name=template.format(*self.node_name(nodes)))

    def _add_all_activation_composite(self, node):
        composite_enzyme = self.graph.predecessors(node) + [self.node_helpers[node]]
        reaction_type_holder = ':{}'
        template = '{}' + reaction_type_holder * (len(composite_enzyme) - 1)
        self.cur_node += 1
        self.node_helpers[tuple(composite_enzyme)] = (self.cur_node,)
        # there is a different composite enzyme because we get U+V+Z+notN -> U:V:Z:N
        composite_enzyme = self.graph.predecessors(node) + [node]
        self._add_node(nodes=composite_enzyme, template=template)

    def activated_separate(self):
        """
        Equations 3.4 from thesis
        :return:
        """
        self.negate_nodes()
        for u, v, d in self.graph.edges(data=True):
            if self._is_all_incoming_edges_are_activation_edges(v):
                reaction_type_holder = ':{}'
                composite_enzyme = [1, 2]  # TODO refactor this is a dummy value
                template = '{}' + reaction_type_holder * (len(composite_enzyme) - 1)
                self.cur_node += 1
                self.node_helpers[(u, self.node_helpers[v])] = (self.cur_node,)
                self._add_node(nodes=[u, v], template=template)

    def activated_combination(self):
        """
        Equations 3.3 from thesis
        :return:
        """
        self.negate_nodes()
        for node in self.graph.nodes():
            if self._is_all_incoming_edges_are_activation_edges(node):
                self._add_all_activation_composite(node)

    def inhibited(self):
        """
        Equations 3.2 from thesis
        """
        self.negate_nodes()
        for node in self.graph.nodes():
            if self._is_all_incoming_edges_are_inhibition_edges(node):
                composite_enzyme = self.graph.predecessors(node) + [node]
                reaction_type_holder = ':{}'
                template = '{}' + reaction_type_holder * (len(composite_enzyme) - 1)
                self.cur_node += 1
                self.node_helpers[tuple(composite_enzyme)] = (self.cur_node,)
                self._add_node(composite_enzyme, template=template)

    def mixed(self):
        """
        Equations 3.1 from thesis
        :return:
        """
        self.negate_nodes()
        for u, v, d in self.graph.edges(data=True):
            if self._is_all_incoming_edges_are_mixed(v):
                reaction_type_holder = ':{}'
                composite_enzyme = [1, 2]  # TODO refactor this is a dummy value
                template = '{}' + reaction_type_holder * (len(composite_enzyme) - 1)
                self.cur_node += 1
                self.node_helpers[(u, v)] = (self.cur_node,)
                self._add_node(nodes=[u, v], template=template)

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
