from stoic.generate_stoic import ExpandGraph
from sampler.sampler import Sampler
from stoic.graph_reader import GraphReader

from examples.engelhardt_et_al import reaction_graph

import argparse
import networkx as nx


def pars():
    p = argparse.ArgumentParser(description='Import graph')
    p.add_argument('node_names', help='file with node names')
    p.add_argument('edge_list', help='file that lists')
    return p


if __name__ == '__main__':
    parser = pars()
    args = parser.parse_args()
    graph = GraphReader(args.node_names, args.edge_list).create_graph()
    expanded_graph = ExpandGraph(graph)  # expand graph
    print "I've deleted rows %s with all zeroes" % expanded_graph.deleted_rows_count
    # feed stoichiometric matrix and reaction vector to EFM Sampler
    r = Sampler(expanded_graph.matrix, expanded_graph.vector)
    # print results
    nx.write_graphml(graph, "imported_graph.graphml")
    nx.write_graphml(expanded_graph.graph, "expanded_graph.graphml")
    # TODO output stoichiometric matrix in SBML format (not sure how)
    # TODO output result # of EFM as a matrix
    # TODO output result # of EFM as txt file with reactions

    # print expanded_graph.vector
    # for reaction in expanded_graph.reactions:
    #     print reaction

    # for r in [r for v, r in zip(expanded_graph.vector, expanded_graph.reactions) if v == 1]:
    #     print r
    print len(expanded_graph.matrix), 'x', len(expanded_graph.matrix[0])

    # look for columns in stoichiometric matrix that have all 0s
    # m = zip(*expanded_graph.matrix)
    # for i, row in enumerate(m):
    #     if all(element == 0 for element in row):
    #         print i, row

    # print('List all reactions')
    # for i, r in enumerate(expanded_graph.reactions, start=1):
    #     print i, r

    r = Sampler(expanded_graph.matrix, expanded_graph.vector)
    print "\nTotal number of EFMs: %s" % len(r.result)
    for i, efms in enumerate(r.result, start=1):
        print 'EFM #%s' % str(i)
        for index, reaction in enumerate(efms):
            if reaction == 1:
                print expanded_graph.human_readable_reaction(expanded_graph.reactions[index])
        print
