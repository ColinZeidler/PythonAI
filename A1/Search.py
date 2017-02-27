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


def bridge_search():
    pass
    start = BridgeState([{'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, 't': 0}, {}])
    end = BridgeState([{}, {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, 't': 0}])

    # This is slow, but gets answer with fewest moves
    bfs = BreadthFirstSearch(start, end)
    node = bfs.runsearch()
    bfs_list = []
    while node.parent is not None:
        bfs_list.append(node.state)
        node = node.parent
    bfs_list.append(node.state)
    bfs_list.reverse()
    print("BFS SEARCH")
    for i in bfs_list:
        print(i)

    # This is fast, but answer may not be fewest moves
    dfs = DepthFirstSearch(start, end)
    node = dfs.runsearch()
    dfs_list = []
    while node.parent is not None:
        dfs_list.append(node.state)
        node = node.parent
    dfs_list.append(node.state)
    dfs_list.reverse()
    print("DFS SEARCH:")
    for i in dfs_list:
        print(i)


def tile_search():
    # get filename to read
    fname = input("file> ")
    with open(fname, 'r') as f:
        # get rows
        rows = int(f.readline())
        # read csv for start
        start = []
        for x in range(rows):
            start.append(f.readline().strip().split(','))
        print("Start: {}".format(start))
        end = []
        for x in range(rows):
            end.append(f.readline().strip().split(','))
        print("End: {}".format(end))
        # read csv for end
    dfs = DepthFirstSearch(TileState(start), TileState(end))
    node = dfs.runsearch()
    l = []
    while node.parent is not None:
        l.append(node.state)
        node = node.parent
    l.append(node.state)
    l.reverse()
    print("DFS SEARCH:")
    for i in l:
        print(i)
    del dfs

    # runs out of memory
    bfs = BreadthFirstSearch(TileState(start), TileState(end))
    node = bfs.runsearch()
    l = []
    while node.parent is not None:
        l.append(node.state)
        node = node.parent
    l.append(node.state)
    l.reverse()
    print("BFS SEARCH:")
    for i in l:
        print(i)


if __name__ == "__main__":
    # bridge_search()
    tile_search()
