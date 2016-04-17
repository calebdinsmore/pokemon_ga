f = open('json/moves.json')
moveDict = eval(''.join(f.readlines()))

f.close()
f = open('json/types.json')
typeDict = eval(''.join(f.readlines()))
