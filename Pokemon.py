# pylint: disable=C
"""Class file defining Pokemon"""

class Pokemon(object):
    def __init__(self, pokeId, name, types, stats, valid_moves, moves):
        self.id = pokeId
        self.name = name
        self.types = types
        self.hp = stats['hp']
        self.attack = stats['attack']
        self.defense = stats['defense']
        self.sp_attack = stats['spattack']
        self.sp_defense = stats['spdefense']
        self.speed = stats['speed']
