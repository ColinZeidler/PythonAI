from Project.Game import PACMAN, BLANK, FOOD, WALL, SPAWN, get_valid_moves
from random import shuffle
MAX_DEPTH = 4
SCORE_MOD = 3
DIST_CUTOFF = -10


class Player(object):
    def __init__(self):
        self.symbol = None
        self.x = 0
        self.y = 0
        self.direction = (0, 0)  # x,y movement vector

    def update_pos(self, x, y, board_o):
        """Copies the input board applies the change, and returns the copy"""
        board = update_board(board_o, (self.x, self.y), (x, y), BLANK, self.symbol)
        self.direction = (x - self.x, y - self.y)
        self.x = x
        self.y = y

        return board

    def find_pos_in_board(self, board):
        for y, row in enumerate(board):
            for x, item in enumerate(row):
                if item == self.symbol:
                    return x, y
        return None

    def calculate_move(self, game):
        """Returns x, y of new position"""
        return self.x, self.y


def update_board(board_o, old_pos, new_pos, old_symbol, new_symbol):
    board = [list(x) for x in board_o]
    board[old_pos[1]][old_pos[0]] = old_symbol
    board[new_pos[1]][new_pos[0]] = new_symbol
    return board


def score_point(board, x, y):
    if board[y][x] == FOOD:
        return 1
    else:
        return 0

class PacMan(Player):
    def __init__(self, x, y):
        super().__init__()
        self.symbol = PACMAN
        self.x = x
        self.y = y

    def calculate_move(self, game):
        """Returns x, y of new position"""
        # should assume ghosts are coming straight towards character
        # wants to collect as much food as possible (move towards a larger group when possible)
        current_state = game.board
        best_score = float("-inf")
        best_move = None
        moves = get_valid_moves(current_state, self.x, self.y)
        shuffle(moves)
        for move in moves:
            new_state = update_board(current_state, (self.x, self.y), move, BLANK, self.symbol)
            p = score_point(new_state, move[0], move[1])
            score = self.min_value(new_state, move, float("-inf"), float("inf"), 1, p, game)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move  # Is only taking the first move

    def max_value(self, board, move, alpha, beta, depth, points_collected, game):
        if depth > MAX_DEPTH:
            h_score = points_collected * SCORE_MOD
            dist_list = []
            for ghost in game.ghosts:
                dist = abs(move[0] - ghost.x) + abs(move[1] - ghost.y)
                dist_list.append(dist)

            dist = min(dist_list)
            dist = DIST_CUTOFF+dist
            h_score += dist
            return h_score
        # generate new moves
        moves = get_valid_moves(board, move[0], move[1])
        shuffle(moves)
        for new_move in moves:
            new_state = update_board(board, move, new_move, BLANK, self.symbol)
            points_collected += score_point(new_state, new_move[0], new_move[1])
            score = self.min_value(new_state, new_move, alpha, beta, depth+1, points_collected, game)
            alpha = max(score, alpha)
            if alpha >= beta:
                return alpha
        return alpha

    def min_value(self, board, move, alpha, beta, depth, points_collected, game):
        if depth > MAX_DEPTH:
            h_score = points_collected * SCORE_MOD
            dist_list = []
            for ghost in game.ghosts:
                dist = abs(move[0] - ghost.x) + abs(move[1] - ghost.y)
                dist_list.append(dist)

            dist = min(dist_list)
            dist = DIST_CUTOFF + dist
            h_score += dist
            return h_score
        # generate new moves
        moves = get_valid_moves(board, move[0], move[1])
        shuffle(moves)
        for new_move in moves:
            new_state = update_board(board, move, new_move, BLANK, self.symbol)
            points_collected += score_point(new_state, new_move[0], new_move[1])
            score = self.max_value(new_state, new_move, alpha, beta, depth+1, points_collected, game)
            beta = min(score, beta)
            if beta <= alpha:
                return beta
        return beta


class MoveNode(object):
    def __init__(self, parent, board, move, pos, cost):
        self.parent = parent
        self.state = board
        self.move = move
        self.pos = pos  # position after move
        self.cost = cost


class Ghost(Player):
    def __init__(self, symbol, x, y):
        super().__init__()
        self.symbol = symbol
        self.x = x
        self.y = y

    def calculate_move(self, game):
        """Returns x, y of new position"""
        # AI algorithm, A* ish
        current_state = game.board
        states = set()
        states.add(repr(current_state))
        target_pos = game.pacman.find_pos_in_board(current_state)
        if target_pos is None:
            return self.x, self.y
        possible_moves = []
        # create possible next moves, each is a top level parent
        for move in get_valid_moves(current_state, self.x, self.y):
            new_state = update_board(current_state,
                                     (self.x, self.y),
                                     move,
                                     BLANK,
                                     self.symbol)
            possible_moves.append(MoveNode(None,
                                           new_state,
                                           move,
                                           move,
                                           1))

        possible_moves = sorted(possible_moves,
                                key=lambda x: abs(x.pos[0]-target_pos[0]) + abs(x.pos[1]-target_pos[1]) + x.cost,
                                reverse=True)
        current_node = possible_moves.pop()

        # Main Search loop
        while current_node.pos != target_pos:
            current_state = current_node.state
            states.add(repr(current_state))
            current_pos = current_node.pos
            moves = get_valid_moves(current_state, current_pos[0], current_pos[1])
            for move in moves:
                new_state = update_board(current_state,
                                         current_pos,
                                         move,
                                         BLANK,
                                         self.symbol)
                if repr(new_state) not in states:
                    possible_moves.append(MoveNode(current_node,
                                                   new_state,
                                                   move,
                                                   move,
                                                   current_node.cost+1))
            possible_moves = sorted(possible_moves,
                                    key=lambda x: abs(x.pos[0]-target_pos[0]) + abs(x.pos[1]-target_pos[1]) + x.cost,
                                    reverse=True)
            if len(possible_moves) > 0:
                current_node = possible_moves.pop()
            else:
                break
        # reached target pos.

        while current_node.parent is not None:
            current_node = current_node.parent

        return current_node.move
