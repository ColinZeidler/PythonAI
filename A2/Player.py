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
    def get_move(self):
        """Looks at the current board state, and calculates best move"""
        pass
