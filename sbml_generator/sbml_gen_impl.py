from sbml_generator.sbml_gen import SBMLGenerator
from stoic.generate_stoic import ExpandGraph
import re


class GenerateSBML(object):

    def __init__(self, graph, reactions):
        self.graph = graph
        self.reactions = reactions
        self.xml_document = self.generate_sbml()

    def generate_sbml(self):
        doc = SBMLGenerator(reactions=self.reactions).document
        model = doc.createModel()
        SBMLGenerator.check(model, 'create model')

        seen_reagents = set()
        for reaction in self.reactions:
            current_reaction = self.add_reaction(model, reaction)
            reactants, products = reaction
            for reagent in reactants:
                species_reference = current_reaction.createReactant()
                self.add_reagents_to_reaction(reagent, species_reference)
                self.add_species(model, reagent, seen_reagents)
            for reagent in products:
                species_reference = current_reaction.createProduct()
                self.add_reagents_to_reaction(reagent, species_reference)
                self.add_species(model, reagent, seen_reagents)
        return doc

    def add_reaction(self, model, reaction):
        current_reaction = model.createReaction()
        reaction_name = ExpandGraph.human_readable_reaction(self.graph, reaction)
        reaction_name = self.replace_non_alphanumeric_with_underscore(reaction_name)
        SBMLGenerator.check(current_reaction.setId(reaction_name), 'set reaction id')
        # SBMLGenerator.check(r1.setReversible(False), 'set reaction reversibility flag')
        return current_reaction

    def add_species(self, model, reagent, seen_reagents):
        if reagent not in seen_reagents:
            species = model.createSpecies()
            name = ExpandGraph.node_name(self.graph, reagent)
            name = self.replace_non_alphanumeric_with_underscore(name)
            SBMLGenerator.check(species.setId(name), 'set species id')
            seen_reagents.add(reagent)

    def add_reagents_to_reaction(self, reagent, species_reference):
        name = ExpandGraph.node_name(self.graph, reagent)
        name = GenerateSBML.replace_non_alphanumeric_with_underscore(name)
        SBMLGenerator.check(species_reference.setSpecies(name), 'assign species')

    @staticmethod
    def replace_non_alphanumeric_with_underscore(string):
        return re.sub('[^0-9a-zA-Z]+', '_', string)
