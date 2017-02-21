from A1.Node import Node
from A1.State import BridgeState, TileState


class Search(object):
    def __init__(self, startstate, targetstate):
        self.visited = []
        self.nodes = [Node(None, startstate)]
        self.targetstate = targetstate

    def addnodes(self, newnodes):
        nodes = [x for x in newnodes if x.state not in self.visited]
        self.nodes.extend(nodes)

    def next(self):
        """empty implement in sub classes"""
        pass

    def runsearch(self):
        currentnode = self.next()
        while currentnode.state != self.targetstate:
            self.visited.append(currentnode.state)
            self.addnodes(currentnode.getchildren())
            currentnode = self.next()

        return currentnode


class BreadthFirstSearch(Search):
    def next(self):
        """Return next item in BFS order"""
        return self.nodes.pop(0)


class DepthFirstSearch(Search):
    def next(self):
        """Return next item in DFS order"""
        return self.nodes.pop(-1)


if __name__ == "__main__":
    start = BridgeState([{1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 't': 0}, {}])
    end = BridgeState([{}, {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 't': 0}])

    # This is slow, but gets answer with fewest moves
    bfs = BreadthFirstSearch(start, end)
    node = bfs.runsearch()
    while node.parent is not None:
        print(node.state)
        node = node.parent
    print(node.state)

    # This is fast, but answer may not be fewest moves
    dfs = DepthFirstSearch(start, end)
    node = dfs.runsearch()
    while node.parent is not None:
        print(node.state)
        node = node.parent
    print(node.state)
