import math
import sys
import os
from player import Player
from tile import Tile

RENT_RATE = 0.1
BUYING_RATE = 0.9
N_TILES = 40

def parse_players(file_name:str) -> list:
    '''
    Parse the player file and return a list of Player objects

    @arguments:
    file_name       -- the name of the players file
    '''
    names = []
    f = open(file_name, 'r')
    index = 0
    while True:
        line = f.readline()
        if line == '':
            break
        line = line.split()
        if len(line[0]) > 8:
            print('Player Names cannot be longer than 8 characters')
            sys.exit()
        try:
            line[1] = int(line[1])
        except:
            print('Amount of money each player has must be an integer between [1, 5000]')
            sys.exit()
        if line[1] < 1 or line[1] > 5000:
            print('Amount of money each player has must be an integer between [1, 5000]')
            sys.exit()
        names.append(Player(line[0],line[1]))

    if len(names) < 2 or len(names) > 4:
        print('Number of players must be between [2, 4]')
        sys.exit()

    return names

def parse_tiles(file_name:str) -> list:
    '''
    Parse the tile file and return a list of Tile objects

    @arguments:
    file_name       -- the name of the tiles file
    '''
    tiles = []
    types = ['GO', 'PROPERTY', 'JAIL', 'GO_TO_JAIL', 'TAX', 'BLANK']
    f = open(file_name, 'r')
    index = 0
    lines = f.read().splitlines()
    sets = [0,0,0]
    while index < len(lines):
        line = lines[index].split()
        j = 0
        exists = False
        while j < len(types):
            if line[0] == types[j]:
                exists = True
            j += 1
        if not exists:
            print(f'Invalid tile type: {line[0]}')
            sys.exit()
        if index == 0 and line[0] != 'GO':
            print('The board must start with a GO tile')
            sys.exit()
        if line[0] == 'GO':
            if sets[0] == 1:
                print('The board must strictly have 1 GO, 1 GO_TO_JAIL and 1 JAIL tiles')
                sys.exit()
            sets[0] = 1
        if line[0] == 'GO_TO_JAIL':
            if sets[1] == 1:
                print('The board must strictly have 1 GO, 1 GO_TO_JAIL and 1 JAIL tiles')
                sys.exit()
            sets[1] = 1
        if line[0] == 'JAIL':
            if sets[2] == 1:
                print('The board must strictly have 1 GO, 1 GO_TO_JAIL and 1 JAIL tiles')
                sys.exit()
            sets[2] = 1

        if len(line) == 3:
            tiles.append(Tile(line[0],line[1],index,line[2]))
        elif len(line) == 2:
            tiles.append(Tile(line[0],line[1],index, 0))
        index += 1

    return tiles

def parse_rolls(file_name:str) -> list:
    '''
    Parse the roll file and return a list of tuples

    Tuples will either be a tuple of two integers or a tuple of the string "PRINT"
    e.g. (2, 4) or ("PRINT")

    @arguments:
    file_name       -- the name of the rolls file
    '''
    rolls = []
    f = open(file_name, 'r')
    while True:
        line = f.readline()
        if line == '':
            break
        line = line.split()
        if len(line) == 1:
            if line != ['PRINT']:
                print(f'Invalid dice roll command: {line[0]}')
                sys.exit()

            rolls.append((line))

        elif len(line) == 2:
            try:
                line[0] = int(line[0])
            except:
                print(f'Invalid dice roll value: {line[0]}')
                sys.exit()
            try:
                line[1] = int(line[1])
            except:
                print(f'Invalid dice roll value: {line[1]}')
                sys.exit()

            if line[0] < 1 or line[0] > 6:
                print(f'Invalid dice roll value: {line[0]}')
                sys.exit()
            if line[1] < 1 or line[1] > 6:
                print(f'Invalid dice roll value: {line[1]}')
                sys.exit()

            rolls.append((line[0], line[1]))
    
    if (rolls[0] != ['PRINT']) or (rolls[len(rolls)-1] != ['PRINT']):
        print('PRINT must be the first and last command in the file')
        sys.exit()

    return rolls

def is_end_game(players:list, rolls:list, roll_index: int) -> bool:
    '''
    The game will end on one of two conditions:
    - One player wins: all but one player is bankrupt
    - Not enough dice rolls: we run out of dice rolls and no one won

    If someone won, print the string 'x won!' where x is the name of the winner
    If not enough dice rolls, print the string 'Not enough dice rolls!'
    Then return True

    Else, return False

    @arguments
    players         -- the list of players
    rolls           -- the list of rolls
    roll_index      -- the index of the current roll we are up to
    '''
    bankrupt = 0
    index = 0
    while index < len(players):
        if players[index].is_bankrupt():
            bankrupt += 1
        index += 1
    if bankrupt == (len(players) - 1):
        index = 0
        while index < len(players):
            if not players[index].is_bankrupt():
                print(f'{players[index].get_name()} won!')
                return True
            index += 1

    if len(rolls) == roll_index:
        print('Not enough dice rolls!')
        return True
    
    return False

def print_status(players:list, tiles:list) -> None:
    header = f'| {"NAME":10}| {"POS":5}| {"BANKRUPT":9}| {"MONEY":7}| {"PROPERTIES":82} |'
    print('-' * len(header))    
    print(header)

    go_index = None
    jail_index = None
    go_to_jail_index = None

    i = 0
    while i < len(tiles):
        if tiles[i].get_tile_type() == 'GO':
            go_index = i
        elif tiles[i].get_tile_type() == 'JAIL':
            jail_index = i
        elif tiles[i].get_tile_type() == 'GO_TO_JAIL':
            go_to_jail_index = i
        i += 1

    i = 0
    while i < len(players):
        # get the Player object
        player = players[i]
        # get the list of Tile objects that this player owns (this is tiles with type "PROPERTY")
        properties = player.get_properties()
        # initialise the string to be 40 dots
        string = ['. '] * N_TILES
        j = 0 
        while j < len(properties):
            property_index = properties[j].get_location_index()
            # replace the corresponding '. ' in the list with house emoji
            string[property_index] = '🏠'
            j += 1
        
        # replace the go, jail, and go_to_jail indexes with emojis 
        # if your list of tiles have not implemented this, then it won't appear
        if go_index is not None:
            string[go_index] =  '⏩' 
        if jail_index is not None:
            string[jail_index] = '🏰'
        if go_to_jail_index is not None:
            string[go_to_jail_index] = '🚓'
        
        # add the square brackets around the joined string
        string = '[' + ''.join(string) + ']'

        print(f'| {player.get_name():10}| {str(player.get_tile_index()):5}| ' \
            f'{str(player.is_bankrupt()):9}| {str(player.get_money()):7}| ' \
            f'{string:42} |')

        i += 1
    print('-' * len(header))

def turn(player, roll, players, tiles, jailTile):
    currentTileIndex = player.get_tile_index() + int(roll[0]) + int(roll[1])
    while currentTileIndex >= N_TILES:
        player.transaction(int(tiles[0].get_cost()))
        currentTileIndex = currentTileIndex - N_TILES
    currentTile = tiles[currentTileIndex]
    player.set_tile_index(currentTileIndex)
    if currentTile.get_tile_type() == 'PROPERTY':
        cost = int(currentTile.get_cost())
        owner = currentTile.find_owner(players)
        if owner == None:
            if abs(cost) < (math.ceil(player.get_money() * BUYING_RATE)):
                player.transaction(cost)
                player.add_property(currentTile)
        else:
            if math.ceil(abs(cost * RENT_RATE)) > player.get_money():
                player.become_bankrupt()
                return False
            else:
                player.pay_rent_to_player(math.floor(cost * RENT_RATE), owner)
    elif currentTile.get_tile_type().strip() == 'TAX':
        cost = int(currentTile.get_cost())
        player.transaction(cost)
    elif currentTile.get_tile_type().strip() == 'GO_TO_JAIL':
        player.set_tile_index(jailTile)
        player.set_jailed(True)
        return False
    
    if player.get_money() < 0:
        player.become_bankrupt()
        return False

    return True

def main():
    '''
    Main function to run the game
    '''
    index = 1
    if len(sys.argv) != 4:
        print("Usage: python3 monopoly.py <PLAYERS> <TILES> <ROLLS>")
        sys.exit()
    while index < len(sys.argv):
        if not os.path.exists(sys.argv[index]):
            print("You have specified an invalid configuration path")
            sys.exit()
        index += 1

    players = parse_players(sys.argv[1])
    tiles = parse_tiles(sys.argv[2])
    rolls = parse_rolls(sys.argv[3])

    index = 0
    jailTile = ''
    while index < len(tiles):
        if tiles[index].get_tile_type() == 'JAIL':
            jailTile = tiles[index].get_location_index()
            break
        index +=1

    index = 0
    player = 0
    while True:
        current = players[player % len(players)]
        if current.is_jailed():
            current.set_jailed(False)
            index -= 1
            player += 1
        elif len(rolls[index]) == 1:
            print_status(players, tiles)
        elif not current.is_bankrupt():
            flag = turn(current, rolls[index], players, tiles, jailTile)

            doubles = 0
            while len(rolls[index]) == 2 and flag:
                if rolls[index][0] == rolls[index][1]:
                    doubles += 1
                    if doubles == 3:
                        current.set_jailed(True)
                        current.set_tile_index(jailTile)
                        break
                    elif (index + 3) < len(rolls):
                        while len(rolls[index + 1]) == 1:
                            if is_end_game(players,rolls,index):
                                print_status(players, tiles)
                                sys.exit()
                            index += 1
                            print_status(players, tiles)
                        
                        if len(rolls[index + 1]) == 2:
                            index += 1
                            if doubles == 2 and rolls[index][0] == rolls[index][1]:
                                current.set_jailed(True)
                                current.set_tile_index(jailTile)
                                break
                            flag = turn(current, rolls[index], players, tiles, jailTile)
                    else:
                        break
                
                else:
                    break
            player += 1
        else:
            index -= 1
            player += 1
        index += 1

        if is_end_game(players,rolls,index):
            print_status(players, tiles)
            sys.exit()

if __name__ == "__main__":
    main()
