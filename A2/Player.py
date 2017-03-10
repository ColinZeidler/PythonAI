"""Author, Colin Zeidler"""


class Player(object):
    def __init__(self, game, id):
        self.game = game
        self.id = id

    def get_move(self):
        """:returns: (source, dest)
        source and dest are tuples as (x, y, count)
        count is the number of pieces to move and is the same for both source and dest
        x is the column
        y is the row"""
        pass


class Human(Player):
    def get_move(self):
        """Prompts the player for input"""
        pass


class Computer(Player):
    def get_move(self):
        """Looks at the current board state, and calculates possible moves"""
        pass
