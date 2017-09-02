import argparse
import csv

import networkx as nx

from sampler.sampler import Sampler
from stoic.generate_stoic import ExpandGraph
from stoic.graph_reader import GraphReader
from sbml_generator.sbml_gen import SBMLGenerator
import re


def pars():
    p = argparse.ArgumentParser(description='Import graph')
    p.add_argument('node_names', help='file with node names')
    p.add_argument('edge_list', help='file that lists')
    return p


def export_reactions_human_readable():
    with open('result/reactions_human.txt', 'w') as f:
        for index, reaction in enumerate(expanded_graph.human_readable_reactions(), start=1):
            f.write("{} {}\n".format(str(index), reaction))


def export_efm_human_readable():
    with open('result/EFM_human.txt', 'w') as f:
        f.write("Total number of EFMs: {}\n".format(len(r.result)))
        for i, efms in enumerate(r.result, start=1):
            f.write('EFM #{}\n'.format(str(i)))
            for index, reaction in enumerate(efms):
                if reaction == 1:
                    f.write('{}\n'.format(expanded_graph.human_readable_reaction(expanded_graph.reactions[index])))
            f.write('\n')


def export_stoichiometric_matrix():
    reaction_count = len(expanded_graph.matrix[0])
    assert len(expanded_graph.graph.nodes()) == len(expanded_graph.matrix)
    with open('result/stoichiometric_matrix.csv', 'w') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
        csv_writer.writerow(['node name'] + ['reaction ' + str(i) for i in range(1, reaction_count + 1)])
        for row, node_name in zip(expanded_graph.matrix, sorted(expanded_graph.graph.nodes(data=True))):
            csv_writer.writerow([str(node_name[1]['name'])] + row)
        csv_writer.writerow(['reversible'] + expanded_graph.vector)


def export_efm_reaction_numbers():
    with open('result/EFM_reactions.txt', 'w') as f:
        f.writelines("Total number of EFMs: %s\n" % len(r.result))
        for i, efms in enumerate(r.result, start=1):
            f.write('EFM #%s\n' % str(i))
            for index, reaction in enumerate(efms):
                if reaction == 1:
                    f.write(str(expanded_graph.reactions[index]))
                    f.write('\n')
            f.write('\n')


def export_sbml(reactions):
    document = generate_sbml(reactions=reactions)
    with open('result/stoichiometric_matrix_in_SBML.xml', "w") as f:
        f.write(SBMLGenerator.convert_to_xml(document=document))


def generate_sbml(reactions):
    doc = SBMLGenerator(reactions=reactions).document
    model = doc.createModel()
    SBMLGenerator.check(model, 'create model')

    seen_reagents = set()
    for reaction in reactions:
        current_reaction = add_reaction(model, reaction)
        reactants, products = reaction
        for reagent in reactants:
            species_reference = current_reaction.createReactant()
            add_reagents_to_reaction(reagent, species_reference)
            add_species(model, reagent, seen_reagents)
        for reagent in products:
            species_reference = current_reaction.createProduct()
            add_reagents_to_reaction(reagent, species_reference)
            add_species(model, reagent, seen_reagents)
    return doc


def add_reaction(model, reaction):
    current_reaction = model.createReaction()
    reaction_name = expanded_graph.human_readable_reaction(reaction)
    reaction_name = replace_non_alphanumeric_with_underscore(reaction_name)
    SBMLGenerator.check(current_reaction.setId(reaction_name), 'set reaction id')
    # SBMLGenerator.check(r1.setReversible(False), 'set reaction reversibility flag')
    return current_reaction


def add_species(model, reagent, seen_reagents):
    if reagent not in seen_reagents:
        species = model.createSpecies()
        name = ExpandGraph.node_name(expanded_graph.graph, reagent)
        name = replace_non_alphanumeric_with_underscore(name)
        SBMLGenerator.check(species.setId(name), 'set species id')
        seen_reagents.add(reagent)


def add_reagents_to_reaction(reagent, species_reference):
    name = ExpandGraph.node_name(expanded_graph.graph, reagent)
    name = replace_non_alphanumeric_with_underscore(name)
    SBMLGenerator.check(species_reference.setSpecies(name), 'assign species')


def replace_non_alphanumeric_with_underscore(string):
    return re.sub('[^0-9a-zA-Z]+', '_', string)


if __name__ == '__main__':
    parser = pars()
    args = parser.parse_args()
    graph = GraphReader(args.node_names, args.edge_list).create_graph()
    expanded_graph = ExpandGraph(graph)  # expand graph
    print("I've deleted rows %s with all zeroes" % expanded_graph.deleted_rows_count)

    export_stoichiometric_matrix()
    export_reactions_human_readable()
    # feed stoichiometric matrix and reaction vector to EFM Sampler
    r = Sampler(expanded_graph.matrix, expanded_graph.vector)

    nx.write_graphml(graph, "result/imported_graph.graphml")
    nx.write_graphml(expanded_graph.graph, "result/expanded_graph.graphml")
    export_sbml(expanded_graph.reactions)
    export_efm_human_readable()
    export_efm_reaction_numbers()

    # print expanded_graph.vector
    # for reaction in expanded_graph.reactions:
    #     print reaction

    # for r in [r for v, r in zip(expanded_graph.vector, expanded_graph.reactions) if v == 1]:
    #     print r

    # print('size of the generated matrix')
    # print(len(expanded_graph.matrix), 'x', len(expanded_graph.matrix[0]))

    # look for columns in stoichiometric matrix that have all 0s
    # m = zip(*expanded_graph.matrix)
    # for i, row in enumerate(m):
    #     if all(element == 0 for element in row):
    #         print i, row

    # print('List all reactions')
    # for i, r in enumerate(expanded_graph.reactions, start=1):
    #     print i, r
