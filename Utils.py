import json

DEBUG = False

f = open('json/moves.json')
f_str = f.read()
moveDict = json.loads(f_str)

moves_to_remove = []
for move_key in moveDict:
    if move_key != "165" and moveDict[move_key]["effect"] != 1:
        moves_to_remove.append(move_key)

f.close()
f = open('json/types.json')
f_str = f.read()
typeDict = json.loads(f_str)

f.close()
f = open('json/pokemon.json')
f_str = f.read()
pokeDict = json.loads(f_str)
pokeList = list(pokeDict.keys())
f.close()

exception_moves = ["89", "94", "85", "188", "309", "348", "405", "412", "414", "431", "454", "533", "566", "583", "53", "57", "58", "280"]

for move in moves_to_remove:
    if move in exception_moves:
        pass
    else:
        for poke in pokeDict:
            move_int = int(move)
            if move_int in pokeDict[poke]["moves"]:
                pokeDict[poke]["moves"].remove(move_int)
        del moveDict[move]

uberList = ['681', '491', '493', '249', '382', '383', '384', '386', '257', '649',
            '150', '717', '716', '643', '645', '644', '658', '487', '484', '483', '722', '250', '289']

print(pokeDict["491"]["moves"])

pokeListSansUbers = list(set(pokeList) - set(uberList))

def printDebug(message, debug=True):
    if debug:
        print(message)
