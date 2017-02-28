import itertools
from copy import deepcopy


class State(object):
    def __init__(self, my_state, cost):
        self.state = my_state
        self.cost = cost

    def build_states(self):
        pass

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        if type(self) is BridgeState:
            return hash(repr([sorted(self.state[0]), sorted(self.state[1])]))
        else:
            return hash(repr(self.state))

    def __str__(self):
        return self.state


class BridgeState(State):
    """State is an array of 2 dicts that match person ids to crossing times, 't' is the torch and has a time of 0
    """
    def build_states(self):
        """Return array of all possible children states"""
        new_states = []
        if 't' in self.state[0]:
            temp = deepcopy(self.state)
            temp[1]['t'] = temp[0].pop('t')
            for pair in itertools.combinations(temp[0], 2):
                temp2 = deepcopy(temp)
                temp2[1][pair[0]] = temp2[0].pop(pair[0])
                temp2[1][pair[1]] = temp2[0].pop(pair[1])
                new_states.append(BridgeState(temp2, max(self.state[0][pair[0]], self.state[0][pair[1]])))
            for k in temp[0].keys():
                temp2 = deepcopy(temp)
                temp2[1][k] = temp2[0].pop(k)
                new_states.append(BridgeState(temp2, self.state[0][k]))
        elif 't' in self.state[1]:
            temp = deepcopy(self.state)
            temp[0]['t'] = temp[1].pop('t')
            for pair in itertools.combinations(temp[1], 2):
                temp2 = deepcopy(temp)
                temp2[0][pair[0]] = temp2[1].pop(pair[0])
                temp2[0][pair[1]] = temp2[1].pop(pair[1])
                new_states.append(BridgeState(temp2, max(self.state[1][pair[0]], self.state[1][pair[1]])))
            for k in temp[1].keys():
                temp2 = deepcopy(temp)
                temp2[0][k] = temp2[1].pop(k)
                new_states.append(BridgeState(temp2, self.state[1][k]))
        return new_states

    def __str__(self):
        return str(self.state[0].keys()) + "--" + str(self.state[1].keys())


class TileState(State):
    def build_states(self):
        """Return array of all possible children states"""
        BLANK = ''
        new_states = []
        blank_x = 0
        blank_y = 0
        max_x = len(self.state)-1
        max_y = len(self.state[0])-1
        my_min = 0
        for x in range(len(self.state)):
            for y in range(len(self.state[x])):
                if self.state[x][y] == BLANK:
                    blank_x = x
                    blank_y = y
                else: # start of chess knight moves
                    for xmove in [2, -2]:
                        for ymove in [1, -1]:
                            x2 = x + xmove
                            y2 = y + ymove
                            if my_min <= x2 <= max_x and my_min <= y2 <= max_y:
                                if self.state[x2][y2] != BLANK:
                                    temp = deepcopy(self.state)
                                    temp[x][y] = self.state[x2][y2]
                                    temp[x2][y2] = self.state[x][y]
                                    new_states.append(TileState(temp, 1))
                    for xmove in [1, -1]:
                        for ymove in [2, -2]:
                            x2 = x + xmove
                            y2 = y + ymove
                            if my_min <= x2 <= max_x and my_min <= y2 <= max_y:
                                if self.state[x2][y2] != BLANK:
                                    temp = deepcopy(self.state)
                                    temp[x][y] = self.state[x2][y2]
                                    temp[x2][y2] = self.state[x][y]
                                    new_states.append(TileState(temp, 1))
                    # end of chess knight moves

        for x in range(blank_x-1, blank_x + 2):
            for y in range(blank_y-1, blank_y + 2):
                if my_min <= x <= max_x and my_min <= y <= max_y:
                    if (x, y) != (blank_x, blank_y):
                        temp = deepcopy(self.state)
                        temp[blank_x][blank_y] = temp[x][y]
                        temp[x][y] = BLANK
                        new_states.append(TileState(temp, 1))

        return new_states

    def __str__(self):
        new_string = "----"
        for row in self.state:
            new_string += "\n" + str(row)
        return new_string


if __name__ == "__main__":
    state = [[8, '', 1], [4, 6, 2], [7, 5, 3]]
    t = TileState(state, 0)
    print("old")
    print(t)
    results = t.build_states()
    print("new")
    for s in results:
        print(s)
