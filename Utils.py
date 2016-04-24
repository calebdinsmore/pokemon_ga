import json

f = open('json/moves.json')
f_str = f.read()
moveDict = json.loads(f_str)

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

uberList = ['681', '491', '493', '249', '382', '383', '384', '386', '257', '649',
            '150', '717', '716', '643', '645', '644', '658', '487', '484', '483']

pokeListSansUbers = list(set(pokeList) - set(uberList))

def printDebug(message, debug=True):
    if debug:
        print(message)
