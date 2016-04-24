# pylint: disable=C

import generateTeam
from operator import itemgetter
import random
from Utils import moveDict, typeDict, pokeDict, pokeList, pokeListSansUbers, uberList
from Pokemon import Pokemon

class Trainer(object):
    def __init__(self, pokemon=None, manual=True):
        if not pokemon:
            self.pokemon = generateTeam.generateTeam()
        else:
            self.pokemon = pokemon
        self.manual = manual
        self.fitness = None

    def tryMutation(self, move_mutation_rate, poke_mutation_rate):
        do_poke_mutation = random.random() < poke_mutation_rate
        do_move_mutation = random.random() < move_mutation_rate

        if do_poke_mutation:
            new_pokemon_key = random.choice(pokeList)
            poke_object = Pokemon(new_pokemon_key, pokeDict[new_pokemon_key]["name"], pokeDict[new_pokemon_key]["types"], pokeDict[new_pokemon_key]["stats"], pokeDict[new_pokemon_key]["moves"])
            poke_object.generateMoves()
            poke_to_mutate = random.choice(self.pokemon)

            poke_object.combineMoves(poke_to_mutate)
        if do_move_mutation:
            poke_to_mutate = random.choice(self.pokemon)
            poke_to_mutate.doMoveMutation()

    def resetPokemon(self):
        for pokemon in self.pokemon:
            pokemon.resetPokemon()

    def calculate_damage(self, move, pokemon_one, pokemon_two):
        move_one = moveDict[move]

        total_type_eff = 0
        move_type = str(move_one["type"])
        if len(pokemon_two.types) == 2:
            type_one = pokemon_two.types[0]
            type_two = pokemon_two.types[1]
            effectiveness_one = typeDict[move_type]["offense"][str(type_one)]
            effectiveness_two = typeDict[move_type]["offense"][str(type_two)]
            total_type_eff = effectiveness_one * effectiveness_two
        else:
            type_one = pokemon_two.types[0]
            total_type_eff = typeDict[move_type]["offense"][str(type_one)]

        if move_type in pokemon_one.types:
            STAB = 1.5
        else:
            STAB = 1

        random_mod = random.randrange(85, 100) / 100

        critical_hit = 1
        if random.random() * 100 <= 6.25:
            critical_hit = 1.5

        modifier = STAB * total_type_eff * critical_hit * random_mod

        attack_stat = 0
        defense_stat = 0
        if moveDict[move]["damage_class"] == "physical":
            attack_stat = pokemon_one.attack
            defense_stat = pokemon_two.attack
        else:
            attack_stat = pokemon_one.sp_attack
            defense_stat = pokemon_two.sp_defense


        damage = (12/250) * ((attack_stat/defense_stat) * move_one["power"] + 2) * modifier
        damage = int(damage)
        return damage

    def get_total_health_percentage(self):
        hp = 0
        total_hp = 0
        for pokemon in self.pokemon:
            if pokemon.current_hp < 0:
                pass
            else:
                hp += pokemon.current_hp
            total_hp += pokemon.total_hp
        return hp/total_hp

    def display_current_pokemon(self, current_pokemon, enemy_pokemon):
        display_string = """
Current Pokemon in Play: %s
    HP: %d / %d""" % (current_pokemon.name, current_pokemon.current_hp, current_pokemon.total_hp)
        print(display_string)

        display_string = """
Enemy Pokemon in Play: %s
    HP: %d / %d""" % (enemy_pokemon.name, enemy_pokemon.current_hp, enemy_pokemon.total_hp)
        print(display_string)

    def display_all_pokemon(self):
        for idx in range(len(self.pokemon)):
            pokemon_string = """
%d. %s
    HP: %d / %d""" % (self.pokemon[idx].name, self.pokemon[idx].current_hp, self.pokemon[idx].total_hp)
            print(pokemon_string)

    def get_type_effectiveness(self, pokemon_one, pokemon_two):
        total_effectiveness = 1
        for poke_type_1 in pokemon_one.types:
            for poke_type_2 in pokemon_two.types:
                total_effectiveness *= typeDict[str(poke_type_1)]["offense"][str(poke_type_2)]
        return total_effectiveness

    def have_better_pokemon(self, current_pokemon, enemy_pokemon):
        for pokemon in self.pokemon:
            if pokemon == current_pokemon or pokemon.current_hp <= 0:
                pass
            else:
                te = self.get_type_effectiveness(pokemon, enemy_pokemon)
                if te >= 2:
                    return True, pokemon
        return False, None

    def get_move(self, current_pokemon, enemy_pokemon):
        if self.manual:
            self.display_current_pokemon(current_pokemon, enemy_pokemon)

            print("Select a choice:\n1. Fight!\n2. Switch Pokemon")
            choice = int(input("=> "))

            if choice == 1:
                for moveId in current_pokemon.moves:
                    moveIdStr = str(moveId)
                    move_string = """
%s. %s
    PP: %d / %d""" % (moveIdStr, current_pokemon.moves[moveIdStr]["name"], current_pokemon.moves[moveIdStr]["current_pp"], current_pokemon.moves[moveIdStr]["pp"])
                    print(move_string)

                move_choice = input("=> ")
                return "move", move_choice
            elif choice == 2:
                self.display_all_pokemon()

                poke_choice = int(input("=> "))
                while self.pokemon[poke_choice] == current_pokemon:
                    print("That pokemon is currently in play.")
                    self.display_all_pokemon()

                return "switch", poke_choice
        else: # AI
            moves_possible = []
            most_damaging = (None, None)
            for moveKey in current_pokemon.moves:
                if current_pokemon.moves[moveKey]["current_pp"] <= 0:
                    pass
                else:
                    damage = self.calculate_damage(str(moveKey), current_pokemon, enemy_pokemon)
                    if most_damaging[0] == None or damage >= most_damaging[1]:
                        most_damaging = (str(moveKey), damage)
            if most_damaging[0] == None: # Struggle
                most_damaging = ("165", self.calculate_damage("165", current_pokemon, enemy_pokemon))
            moves_possible.append([most_damaging[0], most_damaging[1], "move"])

            should_switch = False
            better_poke = None
            te = self.get_type_effectiveness(current_pokemon, enemy_pokemon)
            if te <= 0.5:
                should_switch, better_poke = self.have_better_pokemon(current_pokemon, enemy_pokemon)
            elif te <= 1:
                should_switch, better_poke = self.have_better_pokemon(current_pokemon, enemy_pokemon)

            if should_switch:
                moves_possible.append([better_poke, 20, "switch"])

            moves_possible = sorted(moves_possible, key=itemgetter(1), reverse=True)

            return moves_possible[0][2], moves_possible[0][0]

    def printTeam(self):
        header_string = "%15s  %15s  %15s  %15s  %15s  %15s  %15s" % ("Name", "Type 1", "Type 2", "Move 1", "Move 2", "Move 3", "Move 4")
        print(header_string)
        for pokemon in self.pokemon:
            poke_string = "%15s" % (pokemon.name)
            for typeKey in pokemon.types:
                str_type = str(typeKey)
                poke_string += "  %15s" % (typeDict[str_type]["name"])
            if len(pokemon.types) == 1:
                poke_string += "  %15s" % (" ")
            for moveKey in pokemon.moves:
                poke_string += "  %15s" % (pokemon.moves[moveKey]["name"] + "-" + str(pokemon.moves[moveKey]["power"]))
            print(poke_string)
