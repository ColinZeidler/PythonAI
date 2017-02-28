

class Node(object):
    def __init__(self, parent, state, h_func=None, goal_state=None):
        self.parent = parent
        self.state = state
        self.cost = 0
        self.h_func = h_func
        self.goal_state = goal_state
        if h_func is None:
            self.heuristic = 0
        else:
            self.heuristic = h_func(self.state, goal_state)

    def getchildren(self):
        return [Node(self, x, self.h_func, self.goal_state) for x in self.state.build_states()]
