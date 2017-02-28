from A1.Node import Node
from A1.State import BridgeState, TileState
from collections import deque


class Search(object):
    def __init__(self, startstate, targetstate):
        self.visited = set()
        self.nodes = deque([Node(None, startstate)])
        self.targetstate = targetstate

    def addnodes(self, newnodes):
        nodes = [x for x in newnodes if x.state not in self.visited]
        self.nodes.extend(nodes)

    def next(self):
        """empty implement in sub classes"""
        pass

    def runsearch(self):
        """
        :return: Endstate Node
        """
        currentnode = self.next()
        while currentnode.state != self.targetstate:
            self.visited.add(currentnode.state)
            self.addnodes(currentnode.getchildren())
            currentnode = self.next()
        print("Visited {}, unvisited {}".format(len(self.visited), len(self.nodes)))
        return currentnode


class BreadthFirstSearch(Search):
    def next(self):
        """Return next item in BFS order"""
        return self.nodes.popleft()


class DepthFirstSearch(Search):
    def next(self):
        """Return next item in DFS order"""
        return self.nodes.pop()


class AStarSearch(Search):
    def __init__(self, startstate, endstate, heuristic_func):
        Search.__init__(self, startstate, endstate)
        self.nodes = deque([Node(None, startstate, h_func=heuristic_func, goal_state=endstate)])

    def addnodes(self, newnodes):
        Search.addnodes(self, newnodes)
        self.nodes = sorted(self.nodes, key=lambda x: x.cost + x.heuristic)

    def next(self):
        self.nodes.popleft()


# Bridge Heuristic functions
def bridge_h_1(current_state, goal_state):
    pass


def bridge_h_2(current_state, goal_state):
    pass


def bridge_h_average(current_state, goal_state):
    h = bridge_h_1(current_state, goal_state) + bridge_h_2(current_state, goal_state)
    h /= 2
    return h


# Tile Heuristic functions
def tile_h_1(current_state, goal_state):
    pass


def tile_h_2(current_state, goal_state):
    pass


def tile_h_average(current_state, goal_state):
    h = tile_h_1(current_state, goal_state) + tile_h_2(current_state, goal_state)
    h /= 2
    return h


def bridge_search():
    start = [{}, {}]
    end = [{}, {}]

    print("How many people?")
    count = int(input("> "))

    for i in range(count):
        print("Person {} takes how long to cross?".format(i))
        time = int(input("> "))

        start[0][str(i)] = time
        end[1][str(i)] = time

    start[0]['t'] = 0
    end[1]['t'] = 0
    return BridgeState(start), BridgeState(end)


def tile_search():
    """
    prompts user for input file, and creates start and end states from input data
    :return: TileState(start), TileState(end)
    """
    print("File to read data from:")
    fname = input("> ")
    with open(fname, 'r') as f:
        # get rows
        rows = int(f.readline())
        # read csv for start
        start = []
        for x in range(rows):
            start.append(f.readline().strip().split(','))
        print("Start: {}".format(start))
        # read csv for end
        end = []
        for x in range(rows):
            end.append(f.readline().strip().split(','))
        print("End: {}".format(end))
    return TileState(start), TileState(end)


if __name__ == "__main__":
    print("Choose the problem to run:")
    print("1. Bridge Problem (Commodity Transport)")
    print("2. Tile Problem (Space Management)")
    problem = int(input("> "))

    print("Choose the search to run:")
    print("1. Breadth First Search")
    print("2. Depth First Search")
    print("3. A* heuristic 1")
    print("4. A* heuristic 2")
    print("5. A* heuristic averaging")
    search = int(input("> "))

    start, end = None, None
    if problem == 1:
        start, end = bridge_search()
    elif problem == 2:
        start, end = tile_search()

    s_class = None
    h_func = None
    if search == 1:
        s_class = BreadthFirstSearch(start, end)
    elif search == 2:
        s_class = DepthFirstSearch(start, end)
    elif search == 3:
        if problem == 1:
            h_func = bridge_h_1
        elif problem == 2:
            h_func = tile_h_1
    elif search == 4:
        if problem == 1:
            h_func = bridge_h_2
        elif problem == 2:
            h_func = tile_h_2
    elif search == 5:
        if problem == 1:
            h_func = bridge_h_average
        elif problem == 2:
            h_func = tile_h_average

    if problem >= 3:
        s_class == AStarSearch(start, end, h_func)

    if start is None or end is None or s_class is None:
        print("Bad input")
        exit(-1)

    final_node = s_class.runsearch()
    count = 0
    l = []
    while final_node.parent is not None:
        l.append(final_node.state)
        count += 1
        final_node = final_node.parent

    l.reverse()

    for state in l:
        print(state)
    print("Path to solution took {} nodes".format(count))
