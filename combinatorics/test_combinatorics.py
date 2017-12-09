import networkx as nx
import pytest

from combinatorics.combinatorics import Combinatorics


#
# def setup_module(module):
#     """ setup any state specific to the execution of the given module."""
#     graph = nx.DiGraph()
#
#
# def teardown_module(module):
#     """ teardown any state that was previously setup with a setup_module
#     method.
#     """


@pytest.fixture
def graph():
    g = nx.DiGraph()
    g.add_node(1, name='U')
    return g


@pytest.fixture
def line_graph_activation():
    g = nx.DiGraph()
    g.add_node(1, name='U')
    g.add_node(2, name='N')
    g.add_edge(1, 2, weight=Combinatorics.ACTIVATION)
    return g


@pytest.fixture
def line_graph_inhibition():
    g = nx.DiGraph()
    g.add_node(1, name='V')
    g.add_node(2, name='N')
    g.add_edge(1, 2, weight=Combinatorics.INHIBITION)
    return g


@pytest.fixture
def two_to_one_graph_mix():
    g = nx.DiGraph()
    g.add_node(1, name='U')
    g.add_node(2, name='V')
    g.add_node(3, name='N')
    g.add_edge(1, 3, weight=Combinatorics.ACTIVATION)
    g.add_edge(2, 3, weight=Combinatorics.INHIBITION)
    return g


@pytest.fixture
def two_to_one_graph_activation():
    g = nx.DiGraph()
    g.add_node(1, name='U')
    g.add_node(2, name='V')
    g.add_node(3, name='N')
    g.add_edge(1, 3, weight=Combinatorics.ACTIVATION)
    g.add_edge(2, 3, weight=Combinatorics.ACTIVATION)
    return g


@pytest.fixture
def two_to_one_graph_inhibition():
    g = nx.DiGraph()
    g.add_node(1, name='U')
    g.add_node(2, name='V')
    g.add_node(3, name='N')
    g.add_edge(1, 3, weight=Combinatorics.INHIBITION)
    g.add_edge(2, 3, weight=Combinatorics.INHIBITION)
    return g


@pytest.fixture
def two_to_one_graph_activation_4_nodes():
    g = nx.DiGraph()
    g.add_node(1, name='U')
    g.add_node(2, name='V')
    g.add_node(3, name='N')
    g.add_node(4, name='Z')
    g.add_edge(1, 3, weight=Combinatorics.ACTIVATION)
    g.add_edge(2, 3, weight=Combinatorics.ACTIVATION)
    g.add_edge(4, 3, weight=Combinatorics.ACTIVATION)
    return g


def test_negation_of_all_nodes(graph):
    inst = Combinatorics(graph)
    inst.negate_nodes()
    assert (2, {'name': 'not U'}) in inst.graph.nodes(data=True)


def test_node_helpers_with_one_node(graph):
    inst = Combinatorics(graph)
    inst.negate_nodes()
    assert {1: 2} == inst.node_helpers


def test_mix_integration(two_to_one_graph_mix):
    inst = Combinatorics(two_to_one_graph_mix)
    inst.mixed()
    assert [(1, {'name': 'U'}),
            (2, {'name': 'V'}),
            (3, {'name': 'N'}),
            (4, {'name': 'not U'}),
            (5, {'name': 'not V'}),
            (6, {'name': 'not N'}),
            (7, {'name': 'U:N'}),
            (8, {'name': 'V:N'})] == inst.graph.nodes(data=True)
    assert {1: 4, 2: 5, 3: 6,
            (1, 3): (7,),
            (2, 3): (8,)} == inst.node_helpers


def test_activation_join_dict(two_to_one_graph_mix):
    inst = Combinatorics(two_to_one_graph_mix)
    inst.activated_combination()
    assert [(1, {'name': 'U'}),
            (2, {'name': 'V'}),
            (3, {'name': 'N'}),
            (4, {'name': 'not U'}),
            (5, {'name': 'not V'}),
            (6, {'name': 'not N'})] == inst.graph.nodes(data=True)


def test_activation_join_dict_4_nodes(two_to_one_graph_activation_4_nodes):
    inst = Combinatorics(two_to_one_graph_activation_4_nodes)
    inst.activated_combination()
    assert [(1, {'name': 'U'}),
            (2, {'name': 'V'}),
            (3, {'name': 'N'}),
            (4, {'name': 'Z'}),
            (5, {'name': 'not U'}),
            (6, {'name': 'not V'}),
            (7, {'name': 'not N'}),
            (8, {'name': 'not Z'}),
            (9, {'name': 'U:V:Z:N'})] == inst.graph.nodes(data=True)
    assert {1: 5, 2: 6, 3: 7, 4: 8,
            (1, 2, 4, 7): (9,)} == inst.node_helpers


def test_activaiton_separate(two_to_one_graph_mix):
    inst = Combinatorics(two_to_one_graph_mix)
    inst.mixed()
    assert [(1, {'name': 'U'}),
            (2, {'name': 'V'}),
            (3, {'name': 'N'}),
            (4, {'name': 'not U'}),
            (5, {'name': 'not V'}),
            (6, {'name': 'not N'}),
            (7, {'name': 'U:N'}),
            (8, {'name': 'V:N'})] == inst.graph.nodes(data=True)
    assert {1: 4, 2: 5, 3: 6,
            (1, 3): (7,),
            (2, 3): (8,)} == inst.node_helpers


def test_activation_join(two_to_one_graph_activation):
    inst = Combinatorics(two_to_one_graph_activation)
    inst.activated_separate()
    assert [(1, {'name': 'U'}),
            (2, {'name': 'V'}),
            (3, {'name': 'N'}),
            (4, {'name': 'not U'}),
            (5, {'name': 'not V'}),
            (6, {'name': 'not N'}),
            (7, {'name': 'U:N'}),
            (8, {'name': 'V:N'})] == inst.graph.nodes(data=True)
    assert {1: 4, 2: 5, 3: 6,
            (1, 6): (7,),
            (2, 6): (8,)} == inst.node_helpers


def test_all_inhibition(two_to_one_graph_inhibition):
    inst = Combinatorics(two_to_one_graph_inhibition)
    inst.inhibited()
    assert [(1, {'name': 'U'}),
            (2, {'name': 'V'}),
            (3, {'name': 'N'}),
            (4, {'name': 'not U'}),
            (5, {'name': 'not V'}),
            (6, {'name': 'not N'}),
            (7, {'name': 'U:V:N'})] == inst.graph.nodes(data=True)
