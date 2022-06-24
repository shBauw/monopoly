from __future__ import annotations

'''
NOTE:
You are only required to implement the method bodies of the class.
'''

class Player:

    def __init__(self, name:str, money:int) -> None:
        self.name = name
        self.money = money

        # the properties is initially empty
        self.properties = []

        # each player intially starts at the first tile, so index is 0
        self.tile_index = 0
        
        # each player initially is not in jail (as GO is the first tile)
        self.jailed = False
        self.bankrupt = False

    def get_name(self) -> str:
        '''
        Return the name of the player
        '''
        return self.name

    def get_money(self) -> int:
        '''
        Return the money the player owns
        '''
        return self.money

    def transaction(self, amount:int) -> None:
        '''
        Update the amount of money the player has
 
        @arguments:
        amount             -- the amount to transact, can be positive or negative integer
        '''
        self.money += amount

    def pay_rent_to_player(self, amount:int, player:Player) -> None:
        '''
        Pay rent to another player.

        @arguments:
        amount              -- the amount to pay to another player
        player              -- the player object that you are paying rent to
        '''
        self.transaction(amount)

        player.transaction((amount) * (-1))

    def get_properties(self) -> list:
        '''
        Return the properties the player owns
        '''
        return self.properties

    '''
    Due to cyclical dependency issues, we cannot specify that tile is of type Tile
    However this will make no difference to how the code runs 
    It's just a loss of readability for your sake
    Please read it as 'tile:Tile'
    '''
    def add_property(self, tile:object) -> None:
        '''
        Add a property to the player's properties

        @arguments:
        tile              -- the property to be added
        '''
        self.properties.append(tile)

    def get_tile_index(self) -> int:
        '''
        Return the position (tile index) of the player
        '''
        return self.tile_index

    def set_tile_index(self, tile_index:int) -> None:
        '''
        Update the position (tile_index) of the player

        @arguments;
        tile_index       -- the new position of the player
        '''
        self.tile_index = tile_index

    def is_jailed(self) -> bool:
        '''
        Returns if the player is in jail
        '''
        return self.jailed

    def set_jailed(self, jailed:bool) -> None:
        '''
        Update if the player is jailed or not

        @arguments:
        jailed           -- the new jailing of the player
        '''
        self.jailed = jailed

    def is_bankrupt(self) -> bool:
        '''
        Returns if the player is bankrupt
        '''
        return self.bankrupt

    def become_bankrupt(self) -> None:
        '''
        1. Update the player to be bankrupt
        2. Set their money to 0
        3. Remove all properties owned by this player

        This will mean it will now become available to purchase by other players
        (given that they land on the tile after the property is disowned by this player)
        '''
        self.bankrupt = True
        self.money = 0
        self.properties = []
        self.tile_index = -1
