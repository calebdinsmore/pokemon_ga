# pylint: disable=C
"""Class file defining Pokemon"""
import copy
import random
from Utils import pokeDict, moveDict

def convertToLevel100(stat, HP=False):
    if HP:
        return int(((stat * 2 * 100) / 100) + 110)
    return int(((stat * 2 * 100) / 100) + 5)

class Pokemon(object):
    def __init__(self, pokeId, name, types, stats, valid_moves, moves=None):
        self.id = pokeId
        self.name = name
        self.types = types
        self.current_hp = convertToLevel100(stats['hp'])
        self.total_hp = convertToLevel100(stats['hp'])
        self.attack = convertToLevel100(stats['attack'])
        self.defense = convertToLevel100(stats['defense'])
        self.sp_attack = convertToLevel100(stats['spattack'])
        self.sp_defense = convertToLevel100(stats['spdefense'])
        self.speed = convertToLevel100(stats['speed'])
        self.valid_moves = valid_moves
        self.stats = stats
        if moves:
            self.moves = copy.deepcopy(moves)
        else:
            self.generateMoves()

    def canSwitchToThisFrom(self, current_pokemon):
        return self.current_hp > 0 and self != current_pokemon

    def doMoveMutation(self):
        move_to_replace = random.choice(list(self.moves.keys()))
        del self.moves[move_to_replace]

        new_move = str(random.choice(self.valid_moves))
        cap = 0
        while (moveDict[new_move]["power"] == 0 and cap <= 15) or new_move in self.moves:
            new_move = str(random.choice(self.valid_moves))
            cap += 1
        self.moves[new_move] = moveDict[new_move]
        self.moves[new_move]["current_pp"] = self.moves[new_move]["pp"]

    def generateMoves(self):
        self.moves = {}
        for _ in range(4):
            if len(pokeDict[self.id]["moves"]) <= 4:
                for move_id in pokeDict[self.id]["moves"]:
                    move_id_str = str(move_id)
                    self.moves[move_id_str] = moveDict[move_id_str]
                    self.moves[move_id_str]["current_pp"] = self.moves[move_id_str]["pp"]
            else:
                next_move = str(random.choice(self.valid_moves))
                cap = 0
                while (moveDict[next_move]["power"] == 0 and cap <= 25) or next_move in self.moves:
                    next_move = str(random.choice(self.valid_moves))
                    # print("Next move option: ", moveDict[next_move]["name"])
                    # print("Power option: ", moveDict[next_move]["power"])
                    cap += 1
                # print("Next move choice: ", moveDict[next_move]["name"])
                # print("Power choice: ", moveDict[next_move]["power"])
                # print("Cap: ", cap)
                # print("Pokemon: ", self.name)
                # input()
                self.moves[next_move] = moveDict[next_move]
                self.moves[next_move]["current_pp"] = self.moves[next_move]["pp"]

    def resetPokemon(self):
        for moveKey in self.moves:
            self.moves[moveKey]["current_pp"] = self.moves[moveKey]["pp"]
        self.__init__(self.id, self.name, self.types, self.stats, self.valid_moves, self.moves)

    def combineMoves(self, other_pokemon):
        self.moves.update(other_pokemon.moves)
        keys_to_delete = []
        for moveKey in self.moves:
            if moveKey not in self.valid_moves:
                keys_to_delete.append(moveKey)

        for moveKey in keys_to_delete:
            del self.moves[moveKey]

        while len(self.moves) > 4:
            remove_move = random.choice(list(self.moves.keys()))
            del self.moves[remove_move]
