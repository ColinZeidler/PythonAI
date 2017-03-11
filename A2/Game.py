"""Author, Colin Zeidler"""
from A2.Player import Human, Computer


class Game(object):
    def __init__(self):
        self.p1 = Human(self, "R")
        self.p2 = Computer(self, "G")
        self.board = GameBoard()
        self.board.setup_2player(self.p1, self.p2)

    def play(self):
        keep_playing = True
        while keep_playing:
            # check if p1 owns any towers
            print("Player", self.p1.id, "turn")
            move = self.p1.get_move()
            self.board.apply_move(move)

            # check if p2 owns any towers
            # print("Player", self.p1.id, "turn")
            # move = self.p2.get_move()
            # self.board.apply_move(move)

            if False:
                keep_playing = False

    def ok_pos(self, x, y):

        # Check that pos is within bounds of board
        if x > 7:
            return False
        if y > 7:
            return False
        if x < 0:
            return False
        if y < 0:
            return False

        # check that pos is not in the deleted corners
        if self.board[y][x] is None:
            return False

        return True

    def valid_move(self, move, player_id):
        """:returns: True if the move is a valid move, False otherwise
        Things to check:
        valid start and end positions
        Move distance is <= to number of pieces moving
        Number of pieces moving is <= to number of pieces at starting pos
        Player making move owns the piece at top of the stack"""
        start = move[0]
        dest = move[1]
        if start == dest:
            return False

        xdiff = abs(start[0] - dest[0])
        ydiff = abs(start[1] - dest[1])
        # only allowed to move in one axis
        if xdiff > 0 and ydiff > 0:
            return False

        # total move must be less or equal than the number moving
        if max(xdiff, ydiff) > start[2]:
            return False

        if not self.ok_pos(start[0], start[1]):
            return False
        if not self.ok_pos(dest[0], dest[1]):
            return False

        if start[2] > len(self.board[start[1]][start[0]]):
            return False

        if self.board[start[1]][start[0]][-1] != player_id:
            return False

        return True


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

    def setup_2player(self, p1, p2):
        self.boardState[1][1].append(p1.id)
        self.boardState[1][2].append(p1.id)
        self.boardState[1][3].append(p2.id)
        self.boardState[1][4].append(p2.id)
        self.boardState[1][5].append(p1.id)
        self.boardState[1][6].append(p1.id)

        self.boardState[2][1].append(p2.id)
        self.boardState[2][2].append(p2.id)
        self.boardState[2][3].append(p1.id)
        self.boardState[2][4].append(p1.id)
        self.boardState[2][5].append(p2.id)
        self.boardState[2][6].append(p2.id)

        self.boardState[3][1].append(p1.id)
        self.boardState[3][2].append(p1.id)
        self.boardState[3][3].append(p2.id)
        self.boardState[3][4].append(p2.id)
        self.boardState[3][5].append(p1.id)
        self.boardState[3][6].append(p1.id)

        self.boardState[4][1].append(p2.id)
        self.boardState[4][2].append(p2.id)
        self.boardState[4][3].append(p1.id)
        self.boardState[4][4].append(p1.id)
        self.boardState[4][5].append(p2.id)
        self.boardState[4][6].append(p2.id)

        self.boardState[5][1].append(p1.id)
        self.boardState[5][2].append(p1.id)
        self.boardState[5][3].append(p2.id)
        self.boardState[5][4].append(p2.id)
        self.boardState[5][5].append(p1.id)
        self.boardState[5][6].append(p1.id)

        self.boardState[6][1].append(p2.id)
        self.boardState[6][2].append(p2.id)
        self.boardState[6][3].append(p1.id)
        self.boardState[6][4].append(p1.id)
        self.boardState[6][5].append(p2.id)
        self.boardState[6][6].append(p2.id)

    def setup_4player(self):
        pass

    def apply_move(self, move):
        sx = move[0][0]
        sy = move[0][1]
        dx = move[1][0]
        dy = move[1][1]
        c = move[0][2]
        tmp = self.boardState[sy][sx][-c:]
        del self.boardState[sy][sx][-c:]

        self.boardState[dy][dx].extend(tmp)

        # handle deleting pieces when more than 5 are in one tile
        removed = []
        new_h = len(self.boardState[dy][dx])
        if new_h > 5:
            removed = self.boardState[dy][dx][:new_h-5]
            del self.boardState[dy][dx][:new_h-5]
        # return pieces that get deleted
        return removed

    def __getitem__(self, item):
        return self.boardState[item]

    def __len__(self):
        return len(self.boardState)

    def __str__(self):
        my_string = "     0   1   2   3   4   5   6   7\n"
        for y, row in enumerate(self.boardState):
            my_string += str(y) + " [ "
            for x, item in enumerate(row):
                if item is None:
                    my_string += "XXX "
                else:
                    my_string += str(len(item)) + ":" + str(item[-1] if len(item) > 0 else "X") + " "
            my_string += "]\n"
        return my_string

if __name__ == "__main__":
    print("Starting 2 player game")
    game = Game()
    game.play()
