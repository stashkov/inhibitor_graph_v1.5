from examples.engelhardt_et_al import reaction_graph
from stoic.generate_stoic import ExpandGraph
from sampler.sampler import Sampler

expanded_graph = ExpandGraph(reaction_graph())
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
