# pylint: disable=C

import generateTeam

class Trainer(object):
    def __init__(self, pokemon=None, manual=True):
        if not pokemon:
            self.pokemon = generateTeam.generateTeam()
        else:
            self.pokemon = pokemon
        self.manual = manual

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
