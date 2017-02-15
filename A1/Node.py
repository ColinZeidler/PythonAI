

class Node(object):
    def __init__(self, parent, state):
        self.parent = parent
        self.state = state

    def getchildren(self):
        return [Node(self, x) for x in self.state.buildstates]
