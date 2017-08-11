from examples.engelhardt_et_al import reaction_graph
from stoic.generate_stoic import ExpandGraph

result = ExpandGraph(reaction_graph())
print result.vector
print result.reactions

for r in [r for v, r in zip(result.vector, result.reactions) if v == 1]:
    print r

m = zip(*result.matrix)
for i, row in enumerate(m):
    if all(element == 0 for element in row):
        print i, row
