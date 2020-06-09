class Node:
    def __init__(self, id=None, parent=None):
        self.id = id
        self.parent = parent
        self.children = []

    def add_child(self, node):
        self.children.append(node)


class Graph:
    def __init__(self, node=None):
        if node is None:
            self.root = Node()
        else:
            self.root = node
