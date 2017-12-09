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


def test_mix_integration(two_to_one_graph_mix):
    inst = Combinatorics(two_to_one_graph_mix)
    inst.mixed()
    assert [(1, {'name': 'U'}),
            (2, {'name': 'V'}),
            (3, {'name': 'N'}),
            (4, {'name': 'not N'}),
            (5, {'name': 'U:N'}),
            (6, {'name': 'V:N'})] == inst.graph.nodes(data=True)
    assert {3: 4,
            (1, 3): (5,),
            (2, 3): (6,)} == inst.node_helpers


def test_given_mixed_graph_then_do_nothing(two_to_one_graph_mix):
    inst = Combinatorics(two_to_one_graph_mix)
    inst.activated_combination()
    assert [(1, {'name': 'U'}),
            (2, {'name': 'V'}),
            (3, {'name': 'N'}),
            (4, {'name': 'not N'})] == inst.graph.nodes(data=True)
    assert {3: 4} == inst.node_helpers


def test_activation_join_dict_4_nodes(two_to_one_graph_activation_4_nodes):
    inst = Combinatorics(two_to_one_graph_activation_4_nodes)
    inst.activated_combination()
    assert [(1, {'name': 'U'}),
            (2, {'name': 'V'}),
            (3, {'name': 'N'}),
            (4, {'name': 'Z'}),
            (5, {'name': 'not N'}),
            (6, {'name': 'U:V:Z:N'})] == inst.graph.nodes(data=True)
    assert {3: 5,
            (1, 2, 4, 5): (6,)} == inst.node_helpers


def test_activaiton_separate(two_to_one_graph_mix):
    inst = Combinatorics(two_to_one_graph_mix)
    inst.mixed()
    assert [(1, {'name': 'U'}),
            (2, {'name': 'V'}),
            (3, {'name': 'N'}),
            (4, {'name': 'not N'}),
            (5, {'name': 'U:N'}),
            (6, {'name': 'V:N'})] == inst.graph.nodes(data=True)
    assert {3: 4,
            (1, 3): (5,),
            (2, 3): (6,)} == inst.node_helpers


def test_activation_join(two_to_one_graph_activation):
    inst = Combinatorics(two_to_one_graph_activation)
    inst.activated_separate()
    assert [(1, {'name': 'U'}),
            (2, {'name': 'V'}),
            (3, {'name': 'N'}),
            (4, {'name': 'not N'}),
            (5, {'name': 'U:N'}),
            (6, {'name': 'V:N'})] == inst.graph.nodes(data=True)
    assert {3: 4,
            (1, 4): (5,),
            (2, 4): (6,)} == inst.node_helpers


def test_all_inhibition(two_to_one_graph_inhibition):
    inst = Combinatorics(two_to_one_graph_inhibition)
    inst.inhibited()
    assert [(1, {'name': 'U'}),
            (2, {'name': 'V'}),
            (3, {'name': 'N'}),
            (4, {'name': 'not N'}),
            (5, {'name': 'U:V:N'})] == inst.graph.nodes(data=True)
    assert {3: 4,
            (1, 2, 3): (5,)} == inst.node_helpers
