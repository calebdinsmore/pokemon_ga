# pylint: disable=C
from random import choice
from Pokemon import Pokemon

def generateTeam(tier=''):
    team = []
    uberList = ['681', '491', '493', '249', '382', '383', '384', '386', '257', '649',
                '150', '717', '716', '643', '645', '644', '658', '487', '484', '483']
    f = open('json/pokemon.json')
    pokeList = eval(''.join(f.readlines()))
    f.close()
    if tier == 'uber':
        for i in range(6):
            team.append(choice(uberList))

        finishedTeam = getMoves(team, pokeList)
        return finishedTeam
    else:
        ids = list(set(pokeList.keys()) - set(uberList))
        for i in range(6):
            next_pokemon = choice(ids)
            poke_object = Pokemon(next_pokemon, pokeList[next_pokemon]["name"], pokeList[next_pokemon]["types"], pokeList[next_pokemon]["stats"], pokeList[next_pokemon]["moves"])
            team.append(poke_object)

        finishedTeam = getMoves(team, pokeList)
        return finishedTeam


def getMoves(team, pokeList):
    f = open('json/moves.json')
    moveDict = eval(''.join(f.readlines()))

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
