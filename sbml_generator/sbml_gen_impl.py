from sbml_generator.sbml_gen import SBMLGenerator
from stoic.stoic import ExpandGraph
import re


class GenerateSBML(object):
    """
    Generates XML version in SBML format of reactions.
    Reactions come as list of tuples
    """

    def __init__(self, graph, reactions):
        assert all(isinstance(r, tuple) for r in reactions)
        self.graph = graph
        self.reactions = reactions
        self.doc = SBMLGenerator(reactions=self.reactions).document
        self.model = self.doc.createModel()
        self.seen_reagents = set()

    def generate_sbml(self):
        for reaction in self.reactions:
            current_reaction = self.add_reaction(reaction)
            reactants, products, _ = reaction
            for species in reactants:
                reaction_ref = current_reaction.createReactant()
                self.add_species_to_model(species)
                self.add_species_to_reaction(species, reaction_ref)
            for species in products:
                reaction_ref = current_reaction.createProduct()
                self.add_species_to_model(species)
                self.add_species_to_reaction(species, reaction_ref)
        return self.doc

    def add_reaction(self, reaction):
        _, _, reversibility = reaction
        current_reaction = self.model.createReaction()
        reaction_name = ExpandGraph.human_readable_reaction(self.graph, reaction)
        reaction_name = self.replace_non_alphanumeric_with_underscore(reaction_name)
        SBMLGenerator.check(current_reaction.setId(reaction_name), 'set reaction id')
        SBMLGenerator.check(current_reaction.setReversible(reversibility), 'set reaction reversibility flag')
        return current_reaction

    def add_species_to_model(self, reagent):
        if reagent not in self.seen_reagents:
            species = self.model.createSpecies()
            name = ExpandGraph.node_name(self.graph, reagent)
            name = self.replace_non_alphanumeric_with_underscore(name)
            SBMLGenerator.check(species.setId(name), 'set species id')
            self.seen_reagents.add(reagent)

    def add_species_to_reaction(self, reagent, reaction_reference):
        name = ExpandGraph.node_name(self.graph, reagent)
        name = GenerateSBML.replace_non_alphanumeric_with_underscore(name)
        SBMLGenerator.check(reaction_reference.setSpecies(name), 'assign species')

    @staticmethod
    def replace_non_alphanumeric_with_underscore(string):
        return re.sub('[^0-9a-zA-Z]+', '_', string)
