"""Author, Colin Zeidler"""
MAX_DEPTH = 1


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
        # let the player inspect the board to plan
        planning = True
        while planning:
            print("To view the board type B")
            print("To view a stack type S")
            print("To enter your move type M")
            choice = input("> ").upper()
            if choice == "B":
                print(self.game.board)
            elif choice == "S":
                x, y = get_pos(self.game.ok_pos)
                print("Stack looks like:")
                print("Bottom", self.game.board[y][x], "Top")
            elif choice == "M":
                planning = False
            else:
                print("Invalid Choice")

        # Create move
        planning = True
        while planning:
            # get start location
            print("Start location:")
            start_x, start_y = get_pos(self.game.ok_pos)
            print("Destination")
            dest_x, dest_y = get_pos(self.game.ok_pos)
            count = get_int("Number of pieces to move")
            move = ((start_x, start_y, count), (dest_x, dest_y, count))
            planning = not self.game.valid_move(move, self.id)
            if planning:
                print("Invalid move")
        return move


def get_pos(check_func):
    bad_pos = True
    while bad_pos:
        x = get_int("Column / X")
        y = get_int("Row / Y")
        bad_pos = not check_func(x, y)
        if bad_pos:
            print("Invalid location")
    return x, y


def get_int(text):
    bad = True
    while bad:
        print(text)
        try:
            x = int(input("> "))
            bad = False
        except ValueError:
            print("Enter an integer")
    return x


class Computer(Player):
    def __init__(self, game, id, h_func):
        Player.__init__(self, game, id)
        self.h_func = h_func

    def get_move(self):
        """Looks at the current board state, and calculates best move"""
        children_moves = self.game.get_moves_for_current_player()
        best_move = None
        best_score = -100000
        for move in children_moves:
            score = self.min_value(move, -100000, 100000, 1)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def max_value(self, move, alpha, beta, depth):
        board, killed_items = self.game.board.new_board_from_move(move)
        if depth >= MAX_DEPTH:
            return self.h_func(self, board, killed_items)
        children_moves = self.game.get_moves_for_current_player()
        for c in children_moves:
            t = self.min_value(c, alpha, beta, depth+1)
            alpha = max(alpha, t)
            if alpha >= beta:
                return alpha
        return alpha

    def min_value(self, move, alpha, beta, depth):
        board, killed_items = self.game.board.new_board_from_move(move)
        if depth >= MAX_DEPTH:
            return self.h_func(self, board, killed_items)
        children_moves = self.game.get_moves_for_next_player()
        for c in children_moves:
            t = self.max_value(c, alpha, beta, depth+1)
            beta = min(beta, t)
            if beta <= alpha:
                return beta
        return beta


# heuristic functions for the AI to use
def h_1(player, board, killed_items):
    """diff player owned stacks with opponent stacks"""
    pid = player.id
    count = 0
    for y, row in enumerate(board):
        for x, tile in enumerate(row):
            if tile is None or len(tile) <= 0:
                continue

            if tile[-1] == pid:
                count += 1
            else:
                count -= 1

    for i in killed_items:
        if i != pid:
            count += 1

    return count


def h_2(player, board, killed_items):
    pid = player.id
    count = 0
    for y, row, in enumerate(board):
        for x, tile in enumerate(row):
            if tile is None or len(tile) <= 0:
                continue

            if tile[-1] == pid:
                count += 1*len(tile)  # larger stacks are more valuable
    return count


def h_minimize_opponent(player, board, killed):
    pid = player.id
    score = 0
    for row in board:
        for tile in row:
            if tile is None or len(tile) == 0:
                continue

            if tile[-1] != pid:
                score -= 2
    return score
