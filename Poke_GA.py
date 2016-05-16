# pylint: disable=C

from Trainer import Trainer
from Battle import BattleSim
from Pokemon import Pokemon
from Utils import pokeDict, moveDict
from Plotter import Plotter

import random
import copy
import os
import datetime
import time


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
            trainer.record = []
            for enemyTrainer in self.list_of_opposing_trainers:
                trainer.resetPokemon()
                enemyTrainer.resetPokemon()
                sim = BattleSim(trainer, enemyTrainer)
                trainerHPPercentage, enemyHPPercentage = sim.run_battle()
                battle_result = trainerHPPercentage - enemyHPPercentage
                if battle_result < 0: # if a loss, multiply the negative fitness by 2
                    battle_result *= 2
                trainer.record.append(battle_result)
                trainer.fitness += battle_result

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
        self.calculateAndAssignFitness()
        while self.current_generation < self.epoch_limit and not self.checkForConvergence():
            self.performTournamentAndMating()
            self.calculateAndAssignFitness()

        fittest = self.getFittest()
        # fittest.printTeam()
        # self.list_of_opposing_trainers[0].printTeam()
        # print(fittest.fitness)
        return fittest


first_team_config = [{"id": "493", "moves": ["449", "304", "70", "15"]},    # Normal
                     {"id": "723", "moves": ["449", "280", "411", "337"]},  # Fighting
                     {"id": "724", "moves": ["449", "19", "89", "157"]},    # Flying
                     {"id": "725", "moves": ["449", "188", "398", "85"]},   # Poison
                     {"id": "726", "moves": ["449", "89", "414", "430"]},   # Ground
                     {"id": "727", "moves": ["449", "157", "444", "412"]}]  # Rock

second_team_config = [{"id": "728", "moves": ["449", "404", "19", "304"]},  # Bug
                     {"id": "729", "moves": ["449", "247", "421", "70"]},   # Ghost
                     {"id": "730", "moves": ["449", "430", "247", "19"]},   # Steel
                     {"id": "731", "moves": ["449", "53", "280", "58"]},    # Fire
                     {"id": "732", "moves": ["449", "57", "127", "89"]},    # Water
                     {"id": "733", "moves": ["449", "412", "404", "280"]}]  # Grass

third_team_config = [{"id": "734", "moves": ["449", "85", "87", "398"]},    # Electric
                     {"id": "735", "moves": ["449", "94", "414", "85"]},    # Psychic
                     {"id": "736", "moves": ["449", "58", "59", "70"]},     # Ice
                     {"id": "737", "moves": ["449", "337", "280", "19"]},   # Dragon
                     {"id": "738", "moves": ["449", "399", "430", "449"]},  # Dark
                     {"id": "739", "moves": ["449", "15", "85", "414"]}]    # Fairy

first_team = Trainer(manual=False)
second_team = Trainer(manual=False)
third_team = Trainer(manual=False)

first_team.createTeamFromListOfDicts(first_team_config)
second_team.createTeamFromListOfDicts(second_team_config)
third_team.createTeamFromListOfDicts(third_team_config)

opposing_team_list = [first_team, second_team, third_team]

pg = PokeGA(opposing_team_list)


experiment_dir = 'Experiment-' + datetime.datetime.now().strftime("%m-%d-%Y_%H:%M:%S")
os.mkdir(experiment_dir)
results_file = open(experiment_dir + '/Experiment_Run_Results.txt', 'w')

overall_time_start = time.time()

if pg.draw_graph:
    plotter = Plotter()
for experiment_num in range(1, 2):

    experiment_start = time.time()

    results_file.write("\n\nExperiment Number %d\n%s\n" % (experiment_num, '-'*20))

    fittest_team = None
    for i in range(1, 31):
        print("Iteration: %d" % (i))
        results_file.write("Iteration: %d\n" % (i))

        if fittest_team is not None:
            this_fittest = pg.runAlgorithm(copy.deepcopy(fittest_team))
        else:
            this_fittest = pg.runAlgorithm()

        if pg.draw_graph:
            plotter.addPoint(i, this_fittest.fitness)

        if fittest_team is None or this_fittest.fitness > fittest_team.fitness:
            fittest_team = copy.deepcopy(this_fittest)
            print("New fittest: %f\n\tRecord: %s\n" % (fittest_team.fitness, str(fittest_team.record)))
            results_file.write("New fittest: %f\n\tRecord: %s\n" % (fittest_team.fitness, str(fittest_team.record)))
            fittest_string = fittest_team.printTeam()
            results_file.write(fittest_string)
            fittest_team.resetPokemon()
    results_file.write("Experiment %d duration: %f\n" % (experiment_num, time.time() - experiment_start))
    print("Experiment %d duration: %f" % (experiment_num, time.time() - experiment_start))

    if pg.draw_graph:
        plotter.showPlot(title=experiment_dir + "/Experiment-" + str(experiment_num), save_to_file=True)
        plotter.clearPoints()

    fittest_team.printTeam()
print("Total time spent: ", time.time() - overall_time_start)
input()

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
