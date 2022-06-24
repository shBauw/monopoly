from __future__ import annotations
from player import Player

'''
NOTE:
You are only required to implement the method bodies of the class
'''

class Tile:

    def __init__(self, tile_type:str, name:str, location_index:int, cost:int=None):
        '''
        Tile type is either: GO, PROPERTY, JAIL, GO_TO_JAIL, TAX, BLANK
        '''
        self.tile_type = tile_type
        self.name = name
        
        '''
        The order of the tile on the board, starting from the GO tile which 
        will have an index of 0
        '''
        self.location_index = location_index
        self.cost = cost

    def get_tile_type(self) -> str:
        '''
        Return the type of the property
        '''
        return self.tile_type

    def get_name(self) -> str:
        '''
        Return the name of the property
        '''
        return self.name

    def get_location_index(self) -> int:
        '''
        Return the location index of this tile
        '''
        return self.location_index

    def get_cost(self) -> int:
        '''
        Return the cost of the property
        '''
        return self.cost

    def find_owner(self, players:list) -> Player | None:
        '''
        Return the owner (the player obeject) of the property if it is owned by a player, 
        else return None

        @arguments:
        players             -- the list of player objects in the game
        '''
        index = 0
        while index < len(players):
            properties = players[index].get_properties()
            j = 0
            while j < len(properties):
                if properties[j] == self:
                    return players[index]
                j += 1
            index += 1
        return None
