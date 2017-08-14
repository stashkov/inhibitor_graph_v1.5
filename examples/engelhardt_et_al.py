import networkx as nx


def reaction_graph():
    """
    Original graph can be found in
    supplementary material of
    Engelhardt et al. paper
    """
    g = nx.DiGraph()
    g.add_node(1, name='ACM2')
    g.add_node(2, name='G-Protein beta/gamma')
    g.add_node(3, name='G-Protein alpha-s')
    g.add_node(4, name='GRK 6')
    g.add_node(5, name='G-Protein alpha -o')
    g.add_node(6, name='G-Protein alpha -i')
    g.add_node(7, name='RGS 14')
    g.add_node(8, name='Adenylate cyclase subtypes II/IV/VII')
    g.add_node(9, name='Adenylate cyclase subtypes V/VI')
    g.add_node(10, name='cAMP-GEF1')
    g.add_node(11, name='PKA (cAMP dependent)')
    g.add_node(12, name='GRK 2')
    g.add_node(13, name='cAMP')
    g.add_node(14, name='AMP')
    g.add_node(15, name='Tubulin, Actin')

    g.add_edge(1, 2, weight=0, reaction=1)
    g.add_edge(1, 3, weight=0, reaction=2)
    g.add_edge(1, 6, weight=0, reaction=3)
    g.add_edge(1, 5, weight=0, reaction=4)
    g.add_edge(11, 4, weight=0, reaction=5)
    g.add_edge(11, 7, weight=0, reaction=6)
    g.add_edge(7, 6, weight=1, reaction=7)
    g.add_edge(7, 5, weight=1, reaction=8)
    g.add_edge(3, 9, weight=0, reaction=9)
    g.add_edge(3, 8, weight=0, reaction=9)

    g.add_edge(6, 9, weight=1, reaction=10)

    g.add_edge(2, 8, weight=0, reaction=11)
    g.add_edge(2, 9, weight=1, reaction=11)

    g.add_edge(12, 10, weight=1, reaction=12)
    g.add_edge(11, 12, weight=0, reaction=13)
    g.add_edge(10, 7, weight=0, reaction=14)

    g.add_edge(9, 13, weight=0, reaction=15)
    g.add_edge(8, 13, weight=0, reaction=15)

    g.add_edge(11, 14, weight=0, reaction=16)
    g.add_edge(13, 10, weight=0, reaction=17)
    g.add_edge(13, 14, weight=0, reaction=18)
    g.add_edge(5, 15, weight=0, reaction=19)
    g.add_edge(14, 15, weight=0, reaction=20)
    g.add_edge(12, 15, weight=0, reaction=21)
    g.add_edge(11, 15, weight=0, reaction=22)
    g.add_edge(4, 1, weight=1, reaction=23)
    g.add_edge(13, 11, weight=0, reaction=24)
    g.add_edge(11, 9, weight=1, reaction=25)
    g.add_edge(10, 15, weight=0, reaction=26)

    return g
