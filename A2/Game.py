"""Author, Colin Zeidler"""
from A2.Player import Human, Computer


class Game(object):
    def __init__(self):
        self.p1 = Human(self, 1)
        self.p2 = Computer(self, 2)
        self.board = GameBoard()


class GameBoard(object):
    def __init__(self):
        self.boardState = [[None, None, [], [], [], [], None, None],
                           [None, [], [], [], [], [], [], None],
                           [[], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], []],
                           [None, [], [], [], [], [], [], None],
                           [None, None, [], [], [], [], None, None]
                           ]

    def setup_2player(self):
        pass

    def setup_4player(self):
        pass

    def __str__(self):
        return repr(self.boardState)

if __name__ == "__main__":
    print("Starting 2 player game")
    game = Game()
