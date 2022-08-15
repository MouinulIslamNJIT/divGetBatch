import numpy as np

class BallTree_node:

    def __init__(self, data):
        self.data = np.asarray(data)

        # data should be two-dimensional
        assert self.data.shape[1] == 2

        self.loc = data.mean(0)
        self.radius = np.sqrt(np.max(np.sum((self.data - self.loc) ** 2, 1)))

        self.child1 = None
        self.child2 = None
        self.points = []
        self.height = 0
        self.id = 0

    def __str__(self):
        return "(x=" + str(self.x) + ",y=" + str(self.y) + ")"


class BallTree:
    """Simple Ball tree class"""

    # class initialization function
    def __init__(self, data, treeHeight):
        self.data = np.asarray(data)
        self.treeHeight = treeHeight
        self.nodeIdList = []
        for i in range(2 ** treeHeight):
            self.nodeIdList.append(0)
        self.documentMap = {}

        for i in range(len(data)):
            d = data[i]
            self.documentMap[tuple(d)] = np.zeros(self.treeHeight + 1, dtype=int)

        self.root = self.__buildTree(data, 0)

    def __buildTree(self, data, height):
        print(len(data))
        if height == self.treeHeight:
            return None
        self.nodeIdList[height] = self.nodeIdList[height] + 1
        if len(data) > 1:
            # sort on the dimension with the largest spread
            n = BallTree_node(data)
            n.points = data
            n.height = height
            n.id = self.nodeIdList[height]

            largest_dim = np.argmax(data.max(0) - data.min(0))
            i_sort = np.argsort(data[:, largest_dim])
            data[:] = data[i_sort, :]

            # find split point
            N = data.shape[0]
            half_N = int(N / 2)
            split_point = 0.5 * (data[half_N, largest_dim]
                                 + data[half_N - 1, largest_dim])

            # recursively create subnodes
            n.child1 = self.__buildTree(data[half_N:], n.height + 1)
            n.child2 = self.__buildTree(data[:half_N], n.height + 1)
            return n
        return None

    def traverse(self, node):
        members = []
        if node:
            members += self.traverse(node.child1)
            members.append(node)
            members += self.traverse(node.child2)
        return members