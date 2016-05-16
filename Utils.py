# pylint: disable=C
import json
import copy

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

exception_moves = ["89", "94", "85", "188", "309", "348", "405", "412", "414", "431", "454", "533", "566", "583",
 "53", "57", "58", "280", "299", "9", "8", "428", "399", "242", "340", "19", "247", "396", "157", "430",
 "442", "398", "449", "324", "318", "539", "400", "44", "460", "225", "87", "435", "209", "585", "411", "238",
 "327", "2", "551", "257", "436", "7", "542", "421", "466", "465", "59", "441", "482", "326", "444", "231", "309",
 "211", "152", "127", "503", "61", "496", "29", "163", "547", "245", "158", "34", "253", "342", "440", "482",
 "441", "93", "60", "427", "326", "418", "429", "453", "61", "325", "352", "534"]

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
            '150', '717', '716', '643', '645', '644', '658', '487', '484', '483', '722', '250', '289', '723', '724',
            '725', '726', '727', '728', '729', '730', '731', '732', '733', '734', '735', '736', '737', '738', '739',
            '486']

print(pokeDict["491"]["moves"])

# Generate all Arceus types
currentType = 2
for newId in range(723, 740):
    newIdStr = str(newId)
    pokeDict[newIdStr] = copy.deepcopy(pokeDict["493"])
    pokeDict[newIdStr]['types'] = [currentType]
    pokeDict[newIdStr]['name'] = pokeDict['493']['name'] + '-' + typeDict[str(currentType)]['name']
    currentType += 1

pokeListSansUbers = list(set(pokeList) - set(uberList))

def printDebug(message, debug=True):
    if debug:
        print(message)

def printMovesOfType(move_type=-1, pokemon=None):
    for moveKey in moveDict:
        if move_type == -1 or moveDict[moveKey]['type'] == move_type:
            if pokemon is not None and int(moveKey) in pokeDict[pokemon]['moves']:
                print("%5s %5s %5s %20s" % (moveKey, moveDict[moveKey]['power'], moveDict[moveKey]['accuracy'], moveDict[moveKey]['name']))
            elif pokemon is None:
                print("%5s %5s %5s %20s" % (moveKey, moveDict[moveKey]['power'], moveDict[moveKey]['accuracy'], moveDict[moveKey]['name']))
