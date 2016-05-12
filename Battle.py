# pylint: disable=C
from Trainer import Trainer
from Utils import moveDict, printDebug

class BattleSim(object):
    def __init__(self, team_one, team_two, debug=False):
        self.team_one = team_one
        self.team_two = team_two
        self.t1_selected_poke = None
        self.t2_selected_poke = None
        self.debug = debug

    def game_over(self):
        team_one_dead = True
        team_two_dead = True
        for pokemon in self.team_one.pokemon:
            if pokemon.current_hp > 0:
                team_one_dead = False
                break
        for pokemon in self.team_two.pokemon:
            if pokemon.current_hp > 0:
                team_two_dead = False
                break
        return team_one_dead or team_two_dead

    def execute_move(self, team_one_choice, team_one_pokemon, team_two_pokemon):
        damage = self.team_one.calculate_damage(team_one_choice, team_one_pokemon, team_two_pokemon)
        printDebug("%s used %s! It did %d damage!" % (team_one_pokemon.name, moveDict[team_one_choice]["name"], damage), self.debug)

        team_one_pokemon.damage_dealt += damage

        team_two_pokemon.current_hp -= damage
        if team_one_choice == "165": #Struggle
            team_one_pokemon.current_hp -= team_one_pokemon.total_hp * 0.25
        else:
            team_one_pokemon.moves[team_one_choice]["current_pp"] -= 1

    def switch_pokemon(self, team,  current_poke):
        idx = (team.pokemon.index(current_poke) + 1) % 6

        while team.pokemon[idx].current_hp <= 0 and not self.game_over():
            idx = (idx + 1) % 6

        return team.pokemon[idx]


    def perform_move_exchange_t1_t2(self, team_one_move, team_two_move):
        if self.t1_selected_poke.current_hp > 0:
            self.execute_move(team_one_move, self.t1_selected_poke, self.t2_selected_poke)
        else:
            self.t1_selected_poke = self.switch_pokemon(self.team_one, self.t1_selected_poke)
        if self.t2_selected_poke.current_hp > 0:
            self.execute_move(team_two_move, self.t2_selected_poke, self.t1_selected_poke)
        else:
            self.t2_selected_poke = self.switch_pokemon(self.team_two, self.t2_selected_poke)
        return self.t1_selected_poke, self.t2_selected_poke

    def perform_move_exchange_t2_t1(self, team_two_move, team_one_move):
        if self.t2_selected_poke.current_hp > 0:
            self.execute_move(team_two_move, self.t2_selected_poke, self.t1_selected_poke)
        else:
            self.t2_selected_poke = self.switch_pokemon(self.team_two, self.t2_selected_poke)
        if self.t1_selected_poke.current_hp > 0:
            self.execute_move(team_one_move, self.t1_selected_poke, self.t2_selected_poke)
        else:
            self.t1_selected_poke = self.switch_pokemon(self.team_one, self.t1_selected_poke)
        return self.t2_selected_poke, self.t1_selected_poke

    def run_battle(self):
        self.t1_selected_poke = self.team_one.pokemon[0]
        self.t2_selected_poke = self.team_two.pokemon[0]
        while not self.game_over():
            team_one_choice, team_one_move = self.team_one.get_move(self.t1_selected_poke, self.t2_selected_poke)
            team_two_choice, team_two_move = self.team_two.get_move(self.t2_selected_poke, self.t1_selected_poke)

            if team_one_choice == team_two_choice and team_one_choice == "move":
                if moveDict[team_one_move]["priority"] == moveDict[team_two_move]["priority"]:
                    if self.t1_selected_poke.speed > self.t2_selected_poke.speed:
                        self.t1_selected_poke, self.t2_selected_poke = self.perform_move_exchange_t1_t2(team_one_move, team_two_move)
                    else:
                        self.t2_selected_poke, self.t1_selected_poke = self.perform_move_exchange_t2_t1(team_two_move, team_one_move)
                else:
                    if moveDict[team_one_move]["priority"] > moveDict[team_two_move]["priority"]:
                        self.t1_selected_poke, self.t2_selected_poke = self.perform_move_exchange_t1_t2(team_one_move, team_two_move)
                    else:
                        self.t2_selected_poke, self.t1_selected_poke = self.perform_move_exchange_t2_t1(team_two_move, team_one_move)
            else: #one of them is switching
                if team_one_choice != team_two_choice and team_one_choice == "switch":
                    self.t1_selected_poke = team_one_move
                    printDebug("Team One switched to %s!" % (team_one_move.name), self.debug)
                    self.execute_move(team_two_move, self.t2_selected_poke, self.t1_selected_poke)
                elif team_one_choice != team_two_choice and team_two_choice == "switch":
                    self.t2_selected_poke = team_two_move
                    printDebug("Team Two switched to %s!" % (team_two_move.name), self.debug)
                    self.execute_move(team_one_move, self.t1_selected_poke, self.t2_selected_poke)
                else:
                    self.t1_selected_poke = team_one_move
                    self.t2_selected_poke = team_two_move
            if self.debug:
                input()
        return self.team_one.get_total_health_percentage(), self.team_two.get_total_health_percentage()





# team_one = Trainer(manual=False)
# team_two = Trainer(manual=False)
#
# bs = BattleSim(team_one, team_two)
#
# printDebug("Battle Results:")
# printDebug(bs.run_battle())
