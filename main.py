from examples.engelhardt_et_al import reaction_graph
from stoic.generate_stoic import ExpandGraph
from sampler.sampler import Sampler

result = ExpandGraph(reaction_graph())
print result.vector
print result.reactions

# for r in [r for v, r in zip(result.vector, result.reactions) if v == 1]:
#     print r
print len(result.matrix), 'x', len(result.matrix[0])

# look for columns in stoichiometric matrix that have all 0s
# m = zip(*result.matrix)
# for i, row in enumerate(m):
#     if all(element == 0 for element in row):
#         print i, row

# print('List all reactions')
# for i, r in enumerate(result.reactions, start=1):
#     print i, r

r = Sampler(result.matrix, result.vector)
print "\nTotal number of EFMs: %s" % len(r.result)
for i, efms in enumerate(r.result):
    print 'EFM #%s' % str(i + 1)
    for index, reaction in enumerate(efms):
        if reaction == 1:
            print result.reactions[index]
    print

