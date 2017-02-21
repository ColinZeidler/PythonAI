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
    pass
