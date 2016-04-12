from random import choice

def generateTeam(tier=''):
    team = []
    uberList = ['681', '491', '493', '249', '382', '383', '384', '386', '257', '649', 
                '150', '717', '716', '643', '645', '644', '658', '487', '484', '483']
    f = open('json/pokemon.json')
    pokeList = eval(''.join(f.readlines()))

    if tier == 'uber':
        for i in range(6):
            team.append(choice(uberList))

        finishedTeam = getMoves(team, pokeList)
        return finishedTeam
    else:
        ids = list(set(pokeList.keys()) - set(uberList))
        for i in range(6):
            team.append(choice(ids))

        finishedTeam = getMoves(team, pokeList)
        return finishedTeam


def getMoves(team, pokeList):
    finishedTeam = []

    for pokeId in team:
        chromosome = '{:03}'.format(int(pokeId))
        pokemon = pokeList[pokeId]
        moves = []
        for i in range(4):
            move = choice(pokeList[pokeId]['moves'] )
            while(move in moves):
                move = choice(pokeList[pokeId]['moves'])
            moves.append('{:03}'.format(int(move))) 
            
        finishedTeam.append(chromosome + ''.join(moves))
    return finishedTeam

