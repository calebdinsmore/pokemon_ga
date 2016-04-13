# pylint: disable=C
"""Class file defining Pokemon"""
import copy

class Pokemon(object):
    def __init__(self, pokeId, name, types, stats, valid_moves, moves=None):
        self.id = pokeId
        self.name = name
        self.types = types
        self.current_hp = stats['hp']
        self.total_hp = stats['hp']
        self.attack = stats['attack']
        self.defense = stats['defense']
        self.sp_attack = stats['spattack']
        self.sp_defense = stats['spdefense']
        self.speed = stats['speed']
        self.valid_moves = valid_moves
        if moves:
            self.moves = copy.deepcopy(moves)
