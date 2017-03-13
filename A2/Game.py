"""Author, Colin Zeidler"""
import copy
from A2.Player import Human, Computer, h_diff_vs_opponent, h_max_my_stacks, h_minimize_opponent


class Game(object):
    def __init__(self, p1=None, p2=None):
        # self.p1 = Human(self, "R")
        if p1 is None:
            self.p1 = Computer(self, "R", h_minimize_opponent)
        else:
            self.p1 = p1
            self.p1.game = self
        if p2 is None:
            self.p2 = Computer(self, "G", h_minimize_opponent)
        else:
            self.p2 = p2
            self.p2.game = self
        self.board = GameBoard()
        self.board.setup_2player(self.p1.id, self.p2.id)
        self.current_player = self.p1
        self.next_player = self.p2

    def play(self):
        keep_playing = True
        while keep_playing:
            # check if p1 owns any towers
            self.current_player = self.p1
            self.next_player = self.p2
            if len(self.get_moves_for_current_player()) == 0:
                print("Player", self.current_player.id, "lost")
                keep_playing = False
                continue
            print("Player", self.current_player.id, "turn")
            print(self.board)
            move = self.current_player.get_move()
            self.board.apply_move(move)

            # check if p2 owns any towers
            self.current_player = self.p2
            self.next_player = self.p1
            if len(self.get_moves_for_current_player()) == 0:
                print("Player", self.current_player.id, "lost")
                keep_playing = False
                continue
            print("Player", self.current_player.id, "turn")
            print(self.board)
            move = self.current_player.get_move()
            self.board.apply_move(move)

        print(self.board)

    def get_moves_for_player(self, player_id, board=None):
        moves = []
        state_board = self.board
        if board is not None:
            state_board = board
        for y, row in enumerate(state_board):
            for x, tile in enumerate(row):
                if tile is None or len(tile) <= 0:
                    continue

                if tile[-1] == player_id:
                    for count in range(1, len(tile)+1):
                        for dist in range(1, count+1):
                            m = ((x, y, count), (x+dist, y, count))
                            if self.valid_move(m, player_id, board=state_board):
                                moves.append(m)
                            m = ((x, y, count), (x-dist, y, count))
                            if self.valid_move(m, player_id, board=state_board):
                                moves.append(m)
                            m = ((x, y, count), (x, y+dist, count))
                            if self.valid_move(m, player_id, board=state_board):
                                moves.append(m)
                            m = ((x, y, count), (x, y-dist, count))
                            if self.valid_move(m, player_id, board=state_board):
                                moves.append(m)

        return moves

    def get_moves_for_current_player(self, board=None):
        return self.get_moves_for_player(self.current_player.id, board=board)

    def get_moves_for_next_player(self, board=None):
        return self.get_moves_for_player(self.next_player.id, board=board)

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

    def valid_move(self, move, player_id, board=None):
        """:returns: True if the move is a valid move, False otherwise
        Things to check:
        valid start and end positions
        Move distance is <= to number of pieces moving
        Number of pieces moving is <= to number of pieces at starting pos
        Player making move owns the piece at top of the stack"""
        state_board = self.board
        if board is not None:
            state_board = board
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

        if start[2] > len(state_board[start[1]][start[0]]):
            return False

        if state_board[start[1]][start[0]][-1] != player_id:
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
        self.boardState[1][1].append(p1)
        self.boardState[1][2].append(p1)
        self.boardState[1][3].append(p2)
        self.boardState[1][4].append(p2)
        self.boardState[1][5].append(p1)
        self.boardState[1][6].append(p1)

        self.boardState[2][1].append(p2)
        self.boardState[2][2].append(p2)
        self.boardState[2][3].append(p1)
        self.boardState[2][4].append(p1)
        self.boardState[2][5].append(p2)
        self.boardState[2][6].append(p2)

        self.boardState[3][1].append(p1)
        self.boardState[3][2].append(p1)
        self.boardState[3][3].append(p2)
        self.boardState[3][4].append(p2)
        self.boardState[3][5].append(p1)
        self.boardState[3][6].append(p1)

        self.boardState[4][1].append(p2)
        self.boardState[4][2].append(p2)
        self.boardState[4][3].append(p1)
        self.boardState[4][4].append(p1)
        self.boardState[4][5].append(p2)
        self.boardState[4][6].append(p2)

        self.boardState[5][1].append(p1)
        self.boardState[5][2].append(p1)
        self.boardState[5][3].append(p2)
        self.boardState[5][4].append(p2)
        self.boardState[5][5].append(p1)
        self.boardState[5][6].append(p1)

        self.boardState[6][1].append(p2)
        self.boardState[6][2].append(p2)
        self.boardState[6][3].append(p1)
        self.boardState[6][4].append(p1)
        self.boardState[6][5].append(p2)
        self.boardState[6][6].append(p2)

    def setup_4player(self):
        pass

    def new_board_from_move(self, move):
        """Returns a new GameBoard instance with the move applied. and the items that got deleted
        Does not modify the current object"""
        new_board = GameBoard()
        new_board.boardState = copy.deepcopy(self.boardState)
        deleted = new_board.apply_move(move)
        return new_board, deleted

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

    print("Select Game mode:")
    print("1. Human vs Computer")
    print("2. Computer vs Computer")
    bad_input = True
    while bad_input:
        selction = input("> ")
        try:
            selction = int(selction)
            bad_input = False
            if selction != 1 and selction != 2:
                print("Choose from 1 to 2")
                bad_input = True
        except ValueError:
            print("Enter an Integer")

    print("Select a heuristic for the AI")
    print("1. diff against opponent")
    print("2. maximize my stack count")
    print("3. minimize opponent stack count")
    bad_input = True
    while bad_input:
        h_choice = input("> ")
        try:
            h_choice = int(h_choice)
            bad_input = False
            if h_choice != 1 and h_choice != 2 and h_choice != 3:
                print("Choose from 1 to 3")
                bad_input = True
        except ValueError:
            print("Enter an Integer")
    if h_choice == 1:
        h1 = h_diff_vs_opponent
    if h_choice == 2:
        h1 = h_max_my_stacks
    if h_choice == 3:
        h1 = h_minimize_opponent

    if selction == 1:
        player1 = Human(None, "R")
        player2 = Computer(None, "G", h1)
    elif selction == 2:
        print("Select a heuristic for the second AI")
        print("1. diff against opponent")
        print("2. maximize my stack count")
        print("3. minimize opponent stack count")
        bad_input = True
        while bad_input:
            h_choice = input("> ")
            try:
                h_choice = int(h_choice)
                bad_input = False
                if h_choice != 1 and h_choice != 2 and h_choice != 3:
                    print("Choose from 1 to 3")
                    bad_input = True
            except ValueError:
                print("Enter an Integer")
        if h_choice == 1:
            h2 = h_diff_vs_opponent
        if h_choice == 2:
            h2 = h_max_my_stacks
        if h_choice == 3:
            h2 = h_minimize_opponent
        player1 = Computer(None, "R", h1)
        player2 = Computer(None, "G", h2)

    game = Game(player1, player2)
    game.play()
