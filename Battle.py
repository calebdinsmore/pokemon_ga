# pylint: disable=C
from Trainer import Trainer
from random import *

f = open('json/moves.json')
moveDict = eval(''.join(f.readlines()))

f.close()
f = open('json/types.json')
typeDict = eval(''.join(f.readlines()))

class BattleSim(object):
    def __init__(self, team_one, team_two):
        self.team_one = team_one
        self.team_two = team_two

    def game_over(self):
        team_one_dead = True
        team_two_dead = True
        for pokemon in self.team_one.pokemon:
            if pokemon.current_hp != 0:
                team_one_dead = False
                break
        for pokemon in self.team_two.pokemon:
            if pokemon.current_hp != 0:
                team_two_dead = False
                break
        return team_one_dead or team_two_dead

    def execute_move(self, team_one_choice, team_one_pokemon, team_two_pokemon):
        move_one = moveDict[team_one_choice]

        total_type_eff = 0
        move_type = str(move_one["type"])
        if len(team_two_pokemon.types) == 2:
            type_one = team_two_pokemon.types[0]
            type_two = team_two_pokemon.types[1]
            effectiveness_one = typeDict[move_type]["offense"][str(type_one)]
            effectiveness_two = typeDict[move_type]["offense"][str(type_two)]
            total_type_eff = effectiveness_one * effectiveness_two
        else:
            type_one = team_two_pokemon.types[0]
            total_type_eff = typeDict[move_type]["offense"][str(type_one)]

        if move_type in team_one_pokemon.types:
            STAB = 1.5
        else:
            STAB = 1

        random_mod = randrange(85, 100) / 100

        critical_hit = 1
        if random() * 100 <= 6.25:
            critical_hit = 1.5

        modifier = STAB * total_type_eff * critical_hit * random_mod

        # TODO: Make critical work
        damage = (12/250) * ((team_one_pokemon.attack/team_two_pokemon.defense) * move_one["power"] + 2) * modifier
        damage = int(damage)
        print("Move did %d damage!" % (damage))

        team_two_pokemon.current_hp -= damage
        team_one_pokemon.moves[team_one_choice]["current_pp"] -= 1



    def run_battle(self):
        current_pokemon_team_one = self.team_one.pokemon[0]
        current_pokemon_team_two = self.team_two.pokemon[0]
        while not self.game_over():
            team_one_choice, team_one_move = self.team_one.get_move(current_pokemon_team_one, current_pokemon_team_two)
            team_two_choice, team_two_move = self.team_two.get_move(current_pokemon_team_two, current_pokemon_team_one)

            if team_one_choice == team_two_choice and team_one_choice == "move":
                if moveDict[team_one_move]["priority"] == moveDict[team_two_move]["priority"]:
                    if current_pokemon_team_one.speed > current_pokemon_team_two.speed:
                        self.execute_move(team_one_move, current_pokemon_team_one, current_pokemon_team_two)
                    else:
                        self.execute_move(team_two_move, current_pokemon_team_two, current_pokemon_team_one)
                else:
                    if moveDict[team_one_move]["priority"] > moveDict[team_two_move]["priority"]:
                        self.execute_move(team_one_move, current_pokemon_team_one, current_pokemon_team_two)
                    else:
                        self.execute_move(team_two_move, current_pokemon_team_two, current_pokemon_team_one)
            else: #one of them is switching
            # TODO: Make switching happen
                pass





team_one = Trainer()
team_two = Trainer()

bs = BattleSim(team_one, team_two)

bs.run_battle()
