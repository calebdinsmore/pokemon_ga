# pylint: disable=C

from Trainer import Trainer
from Battle import BattleSim
from Pokemon import Pokemon
from Utils import pokeDict, moveDict
from Plotter import Plotter

import random
import copy

class PokeGA(object):
    def __init__(self, listOfOpposingTrainers=[]):
        self.poke_mutation_rate = 0.005
        self.move_mutation_rate = 0.01
        self.crossover_rate = 0.6
        self.points_of_crossover = 1
        self.population_size = 20
        self.epoch_limit = 10000
        self.draw_graph = False
        self.current_generation = 0
        self.list_of_opposing_trainers = listOfOpposingTrainers
        self.convergence_array = []

        self.winning_pokemon_dict = {}

        self.chromosomes = []

        self.parseConfig()

        for _ in range(6):
            self.convergence_array.append(False)


    def parseConfig(self):
        config = open("config.txt", "r")
        for line in config:
            lineSpl = line.split()
            exec("self." + lineSpl[0] + lineSpl[1])

    def generateStartingPopulation(self):
        for _ in range(self.population_size):
            self.chromosomes.append(Trainer(manual=False))

    def calculateAndAssignFitness(self):
        for trainer in self.chromosomes:
            trainer.fitness = 0
            for enemyTrainer in self.list_of_opposing_trainers:
                trainer.resetPokemon()
                enemyTrainer.resetPokemon()
                sim = BattleSim(trainer, enemyTrainer)
                trainerHPPercentage, enemyHPPercentage = sim.run_battle()
                trainer.fitness += trainerHPPercentage - enemyHPPercentage

    def compareFitnesses(self, cand_one, cand_two):
        chosen_parent = None
        if cand_one.fitness > cand_two.fitness:
            chosen_parent = cand_one
        else:
            chosen_parent = cand_two
        return chosen_parent

    def getMatingCandidatesAndReturnChoice(self):
        first_candidate = random.choice(self.chromosomes)
        self.chromosomes.remove(first_candidate)
        second_candidate = random.choice(self.chromosomes)
        self.chromosomes.remove(second_candidate)
        chosen_parent = self.compareFitnesses(first_candidate, second_candidate)
        self.chromosomes.append(first_candidate)
        self.chromosomes.append(second_candidate)
        return chosen_parent

    def mateParents(self, parent_one, parent_two):
        doCrossover = random.random() < self.crossover_rate
        if doCrossover:
            crossoverPoint = random.randrange(0, 6)
            return self.performCrossover(crossoverPoint, parent_one, parent_two)
        else:
            return parent_one, parent_two

    def performCrossover(self, crossoverPoint, parent_one, parent_two):
        offspring_one_pokemon = parent_one.pokemon[:crossoverPoint] + parent_two.pokemon[crossoverPoint:]
        offspring_two_pokemon = parent_two.pokemon[:crossoverPoint] + parent_one.pokemon[crossoverPoint:]

        fittest = self.getFittest()

        if parent_one != fittest:
            parent_one.pokemon = offspring_one_pokemon
        if parent_two != fittest:
            parent_two.pokemon = offspring_two_pokemon

        return parent_one, parent_two

    def performTournamentAndMating(self):
        next_generation = []
        while len(next_generation) < self.population_size:
            parent_one = self.getMatingCandidatesAndReturnChoice()
            parent_two = self.getMatingCandidatesAndReturnChoice()

            offspring_one, offspring_two = self.mateParents(parent_one, parent_two)

            offspring_one.resetPokemon()
            offspring_two.resetPokemon()

            if offspring_one != parent_one: # offspring is fittest
                offspring_one.tryMutation(self.move_mutation_rate, self.poke_mutation_rate)
            if offspring_two != parent_two:
                offspring_two.tryMutation(self.move_mutation_rate, self.poke_mutation_rate)

            next_generation.append(offspring_one)
            next_generation.append(offspring_two)
        self.current_generation += 1
        self.chromosomes = next_generation

    def checkForConvergence(self):
        for geneIdx in range(len(self.convergence_array)):
            poke_ids = []
            for trainer in self.chromosomes:
                poke_ids.append(trainer.pokemon[geneIdx].id)
            poke_ids.sort()
            self.convergence_array[geneIdx] = poke_ids.count(poke_ids[self.population_size // 2]) / self.population_size >= 0.97
        if self.convergence_array.count(True) == 6:
            return True
        else:
            return False

    def getFittest(self):
        fitList = []
        for chrom in self.chromosomes:
            fitList.append((chrom.fitness, chrom))
        maxTup = max(fitList,key=lambda item:item[0])
        return maxTup[1]

    def runAlgorithm(self, seed=None):
        self.generateStartingPopulation()
        if seed is not None:
            self.chromosomes.pop(-1)
            self.chromosomes.append(seed)
        if self.draw_graph:
            plotter = Plotter()
        self.calculateAndAssignFitness()
        while self.current_generation < self.epoch_limit and not self.checkForConvergence():
            self.performTournamentAndMating()
            self.calculateAndAssignFitness()
            if self.draw_graph:
                fittest = self.getFittest()
                plotter.addPoint(self.current_generation, fittest.fitness)

        fittest = self.getFittest()
        # fittest.printTeam()
        # self.list_of_opposing_trainers[0].printTeam()
        if self.draw_graph:
            plotter.showPlot()
        # print(fittest.fitness)
        return fittest


# team_config = {"385": ["Dazzling Gleam", "Iron Head", "Ice Punch", "Signal Beam"], "442", "382", "202", "150", "483"}
first_team_config = [{"id": "722", "moves": ["618", "53", "57", "58"]},
                     {"id": "722", "moves": ["618", "85", "89", "304"]},
                     {"id": "722", "moves": ["618", "337", "412", "53"]},
                     {"id": "722", "moves": ["618", "57", "58", "337"]},
                     {"id": "722", "moves": ["618", "412", "85", "304"]},
                     {"id": "722", "moves": ["618", "85", "89", "53"]}]
second_team_config = [{"id": "483", "moves": ["53", "58", "85", "408"]},
                     {"id": "487", "moves": ["85", "89", "94", "414"]},
                     {"id": "150", "moves": ["53", "58", "412", "94"]},
                     {"id": "257", "moves": ["280", "53", "89", "64"]},
                     {"id": "491", "moves": ["58", "188", "280", "94"]},
                     {"id": "722", "moves": ["618", "85", "89", "53"]}]

first_team = Trainer(manual=False)
second_team = Trainer(manual=False)

first_team.createTeamFromListOfDicts(first_team_config)
second_team.createTeamFromListOfDicts(second_team_config)

opposing_team_list = [first_team, second_team]

pg = PokeGA(opposing_team_list)

fittest_team = None

for i in range(30):
    print("Iteration: ", i)
    this_fittest = pg.runAlgorithm(copy.deepcopy(fittest_team))

    if fittest_team is None or this_fittest.fitness > fittest_team.fitness:
        fittest_team = copy.deepcopy(this_fittest)
        print("New fittest: ", fittest_team.fitness)
        fittest_team.printTeam()
        fittest_team.resetPokemon()

fittest_team.printTeam()

# fittest_team.resetPokemon()
# opposing_team_list[0].resetPokemon()
# fittest_team.debug = True
# opposing_team_list[0].debug = True
#
# bs = BattleSim(fittest_team, opposing_team_list[0], debug=True)
#
# bs.run_battle()


    # for pokemon in fittest.pokemon:
    #     if pokemon.name in pg.winning_pokemon_dict:
    #         pg.winning_pokemon_dict[pokemon.name]["times_used"] += 1
    #         for move in pokemon.moves:
    #             if move in pg.winning_pokemon_dict[pokemon.name]["moves"]:
    #                 pg.winning_pokemon_dict[pokemon.name]["moves"][move]["times_used"] += 1
    #             else:
    #                 pg.winning_pokemon_dict[pokemon.name]["moves"][move] = {"times_used": 1}
    #     else:
    #         pg.winning_pokemon_dict[pokemon.name] = {"times_used": 1, "moves": {}}
    #         for move in pokemon.moves:
    #             if move in pg.winning_pokemon_dict[pokemon.name]["moves"]:
    #                 pg.winning_pokemon_dict[pokemon.name]["moves"][move]["times_used"] += 1
    #             else:
    #                 pg.winning_pokemon_dict[pokemon.name]["moves"][move] = {"times_used": 1}

# times_used_list = []
# for pokemon in pg.winning_pokemon_dict:
#     times_used_list.append((pokemon, pg.winning_pokemon_dict[pokemon]["times_used"]))
#
# times_used_list = sorted(times_used_list,key=lambda item:item[1], reverse=True)
#
# print("%20s %20s" % ("Pokemon Name", "Times Used"))
# for pokemon_tup in times_used_list:
#     poke_string = "%20s %20d" % (pokemon_tup[0], pg.winning_pokemon_dict[pokemon_tup[0]]["times_used"])
#     print(poke_string)
#
# print("%20s %20s %20s" % ("Pokemon Name", "Move Name", "Times Used"))
# for pokemon in pg.winning_pokemon_dict:
#     print("%20s" % (pokemon))
#     for move in pg.winning_pokemon_dict[pokemon]["moves"]:
#         move_string = "%20s %20s %20s" % (" ", moveDict[move]["name"], pg.winning_pokemon_dict[pokemon]["moves"][move]["times_used"])
#         print(move_string)
