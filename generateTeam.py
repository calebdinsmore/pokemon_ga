# pylint: disable=C
from random import choice
from Pokemon import Pokemon

from Utils import uberList, pokeDict, moveDict

def generateTeam(tier=''):
    team = []
    if tier == 'uber':
        for _ in range(6):
            next_pokemon = choice(uberList)
            poke_object = Pokemon(next_pokemon, pokeDict[next_pokemon]["name"], pokeDict[next_pokemon]["types"], pokeDict[next_pokemon]["stats"], pokeDict[next_pokemon]["moves"])
            team.append(poke_object)

        finishedTeam = getMoves(team)
        return finishedTeam
    else:
        ids = list(set(pokeDict.keys()) - set(uberList))
        for _ in range(6):
            next_pokemon = choice(ids)
            poke_object = Pokemon(next_pokemon, pokeDict[next_pokemon]["name"], pokeDict[next_pokemon]["types"], pokeDict[next_pokemon]["stats"], pokeDict[next_pokemon]["moves"])
            team.append(poke_object)

        finishedTeam = getMoves(team)
        return finishedTeam


def getMoves(team):
    for pokemon in team:
        poke_id = pokemon.id
        moves = {}
        for _ in range(4):
            if len(pokeDict[poke_id]["moves"]) < 4:
                for move_id in pokeDict[poke_id]["moves"]:
                    move_id_str = str(move_id)
                    moves[move_id_str] = moveDict[move_id_str]
                    moves[move_id_str]["current_pp"] = moves[move_id_str]["pp"]
            else:
                next_move = str(choice(pokeDict[poke_id]["moves"]))
                while next_move in moves:
                    next_move = str(choice(pokeDict[poke_id]["moves"]))
                moves[next_move] = moveDict[next_move]
                moves[next_move]["current_pp"] = moves[next_move]["pp"]

            pokemon.moves = moves
    return team
