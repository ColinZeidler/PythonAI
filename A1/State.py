

class State(object):
    def __init__(self, state):
        self.state = state  # state is a string of characters

    def buildstates(self):
        pass

    def __eq__(self, other):
        return self.state == other.state


class BridgeState(State):
    def buildstates(self):
        """Return array of all possible children states"""
        pass


class TileState(State):
    def buildstates(self):
        """Return array of all possible children states"""
        pass
