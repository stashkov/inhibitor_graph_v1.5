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

    def activated_separate(self):
        """
        Equations 3.4 from thesis
        :return:
        """
        for u, v, d in self.graph.edges(data=True):
            if self._is_all_incoming_edges_are_activation_edges(v):
                composite_enzyme = [u, v]
                self.cur_node += 1
                self.node_helpers[(u, self.node_helpers[v])] = (self.cur_node,)
                self._add_node(nodes=composite_enzyme, template=(self._template(composite_enzyme)))

    def activated_combination(self):
        """
        Equations 3.3 from thesis
        :return:
        """
        for node in self.graph.nodes():
            if self._is_all_incoming_edges_are_activation_edges(node):
                composite_enzyme = self.graph.predecessors(node) + [self.node_helpers[node]]
                self.cur_node += 1
                self.node_helpers[tuple(composite_enzyme)] = (self.cur_node,)
                # there is a different composite enzyme because we get U+V+Z+notN -> U:V:Z:N
                composite_enzyme = self.graph.predecessors(node) + [node]
                self._add_node(nodes=composite_enzyme, template=(self._template(composite_enzyme)))

    def inhibited(self):
        """
        Equations 3.2 from thesis
        """
        for node in self.graph.nodes():
            if self._is_all_incoming_edges_are_inhibition_edges(node):
                composite_enzyme = self.graph.predecessors(node) + [node]
                self.cur_node += 1
                self.node_helpers[tuple(composite_enzyme)] = (self.cur_node,)
                self._add_node(nodes=composite_enzyme, template=(self._template(composite_enzyme)))

    def _template(self, composite_enzyme):
        template = '{}' + ':{}' * (len(composite_enzyme) - 1)
        return template

    def mixed(self):
        """
        Equations 3.1 from thesis
        :return:
        """
        for u, v, d in self.graph.edges(data=True):
            if self._is_all_incoming_edges_are_mixed(v):
                composite_enzyme = [u, v]
                self.cur_node += 1
                self.node_helpers[tuple(composite_enzyme)] = (self.cur_node,)
                self._add_node(nodes=composite_enzyme, template=(self._template(composite_enzyme)))

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

    def _add_node(self, nodes, template):
        self.graph.add_node(self.cur_node, name=template.format(*self._node_name(nodes)))

    def _node_name(self, nodes):
        if isinstance(nodes, int):
            return self.graph.node[nodes]['name']
        if isinstance(nodes, list):
            return [self.graph.node[node]['name'] for node in nodes]
