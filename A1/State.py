import itertools
from copy import deepcopy


class State(object):
    def __init__(self, state):
        self.state = state

    def buildstates(self):
        pass

    def __eq__(self, other):
        return self.state == other.state

    def __str__(self):
        return self.state


class BridgeState(State):
    """State is an array of 2 dicts that match person ids to crossing times, 't' is the torch and has a time of 0
    """
    def buildstates(self):
        """Return array of all possible children states"""
        new_states = []
        if 't' in self.state[0]:
            temp = deepcopy(self.state)
            temp[1]['t'] = temp[0].pop('t')
            for pair in itertools.combinations(temp[0], 2):
                temp2 = deepcopy(temp)
                temp2[1][pair[0]] = temp2[0].pop(pair[0])
                temp2[1][pair[1]] = temp2[0].pop(pair[1])
                new_states.append(BridgeState(temp2))
            for k in temp[0].keys():
                temp2 = deepcopy(temp)
                temp2[1][k] = temp2[0].pop(k)
                new_states.append(BridgeState(temp2))
        elif 't' in self.state[1]:
            temp = deepcopy(self.state)
            temp[0]['t'] = temp[1].pop('t')
            for pair in itertools.combinations(temp[1], 2):
                temp2 = deepcopy(temp)
                temp2[0][pair[0]] = temp2[1].pop(pair[0])
                temp2[0][pair[1]] = temp2[1].pop(pair[1])
                new_states.append(BridgeState(temp2))
            for k in temp[1].keys():
                temp2 = deepcopy(temp)
                temp2[0][k] = temp2[1].pop(k)
                new_states.append(BridgeState(temp2))
        return new_states

    def __str__(self):
        return str(self.state[0].keys()) + "--" + str(self.state[1].keys())


class TileState(State):
    def buildstates(self):
        """Return array of all possible children states"""
        pass
