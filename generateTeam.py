# pylint: disable=C
from random import choice
from Pokemon import Pokemon

from Utils import uberList
import json

f = open('json/pokemon.json')
f_str = f.read()
pokeList = json.loads(f_str)


f = open('json/moves.json')
f_str = f.read()
moveDict = json.loads(f_str)

def generateTeam(tier=''):
    team = []
    f.close()
    if tier == 'uber':
        for _ in range(6):
            next_pokemon = choice(uberList)
            poke_object = Pokemon(next_pokemon, pokeList[next_pokemon]["name"], pokeList[next_pokemon]["types"], pokeList[next_pokemon]["stats"], pokeList[next_pokemon]["moves"])
            team.append(poke_object)

        finishedTeam = getMoves(team, pokeList)
        return finishedTeam
    else:
        ids = list(set(pokeList.keys()) - set(uberList))
        for _ in range(6):
            next_pokemon = choice(ids)
            poke_object = Pokemon(next_pokemon, pokeList[next_pokemon]["name"], pokeList[next_pokemon]["types"], pokeList[next_pokemon]["stats"], pokeList[next_pokemon]["moves"])
            team.append(poke_object)

        finishedTeam = getMoves(team, pokeList)
        return finishedTeam


def getMoves(team, pokeList):
    for pokemon in team:
        poke_id = pokemon.id
        moves = {}
        for _ in range(4):
            if len(pokeList[poke_id]["moves"]) < 4:
                for move_id in pokeList[poke_id]["moves"]:
                    move_id_str = str(move_id)
                    moves[move_id_str] = moveDict[move_id_str]
                    moves[move_id_str]["current_pp"] = moves[move_id_str]["pp"]
            else:
                next_move = str(choice(pokeList[poke_id]["moves"]))
                while next_move in moves:
                    next_move = str(choice(pokeList[poke_id]["moves"]))
                moves[next_move] = moveDict[next_move]
                moves[next_move]["current_pp"] = moves[next_move]["pp"]

            pokemon.moves = moves
    return team
