

# DEFS
SPAWN = 'S'
PACMAN = 'P'
WALL = 'X'
FOOD = 'o'
BLANK = ' '
# END DEFS


class Game(object):
    def __init__(self, ghost_list, board_file="map.txt"):
        self.board = load_board_state(board_file)
        self.pacman = self.spawn_pacman()
        self.score = 0
        self.turn = 0
        self.ghosts = self.spawn_ghosts(ghost_list)

    def play_game(self):
        """This is the main game play loop"""
        play_game = True
        self.turn = 0
        while play_game:
            x, y = self.pacman.calculate_move(self)
            self.score_point(x, y)
            self.board = self.pacman.update_pos(x, y, self.board)

            for ghost in self.ghosts:
                x, y = ghost.calculate_move(self)
                self.board = ghost.update_pos(x, y, self.board)

            # check if PacMan was killed
            found = self.pacman.find_pos_in_board(self.board)
            if found is None:
                play_game = False

            self.print_game_state()
            self.turn += 1
        print("Game Over, PacMan is Dead")

    def score_point(self, x, y):
        if self.board[y][x] == FOOD:
            self.score += 1

    def print_game_state(self):
        print("Turn: {}, Score: {}".format(self.turn, self.score))
        for row in self.board:
            print("".join(row))

    def spawn_pacman(self):
        from Project.Players import PacMan
        for y, row in enumerate(self.board):
            for x, item in enumerate(row):
                if item == PACMAN:
                    pacman = PacMan(x, y)
                    return pacman

    def spawn_ghosts(self, ghost_list):
        from Project.Players import Ghost
        ghosts = []
        for ghost in ghost_list:
            found = False
            for y, row in enumerate(self.board):
                if not found:
                    for x, item in enumerate(row):
                        if item == SPAWN:
                            found = True
                            self.board[y][x] = ghost
                            ghosts.append(Ghost(ghost, x, y))
                            break

        for y, row in enumerate(self.board):
            for x, item in enumerate(row):
                if item == SPAWN:
                    self.board[y][x] = BLANK
        return ghosts


def get_valid_moves(board, x, y):
    """Input current position of character
    Output all possible new positions"""
    moves = []
    if board[y][x+1] != WALL:
        moves.append((x+1, y))
    if board[y][x-1] != WALL:
        moves.append((x-1, y))
    if board[y+1][x] != WALL:
        moves.append((x, y+1))
    if board[y-1][x] != WALL:
        moves.append((x, y-1))
    return moves


def load_board_state(file_name):
    """
    o = food / point thing
    X = wall
    P = pac man
    S = ghost spawn
    ' ' = empty space
    """

    board = []

    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip()
            board.append(list(line))
    return board

if __name__ == "__main__":
    game = Game(['1', '2', '3'], "map.txt")
    game.play_game()
