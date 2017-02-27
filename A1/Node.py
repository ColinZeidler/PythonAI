

class Node(object):
    def __init__(self, parent, state):
        self.parent = parent
        self.state = state
        self.cost = 0
        self.heuristic = 0

    def getchildren(self):
        return [Node(self, x) for x in self.state.build_states()]
