from typing import Dict, Tuple, List, Set
import numpy as np


class Node:
    def __init__(self,
                 identifier: str = None,
                 odour: np.array = None):
        if odour is None:
            odour = np.array([])
        self.identifier = str(identifier)
        self.odour = odour

    def __repr__(self):
        return self.identifier

    def __str__(self):
        return '{id: ' + self.identifier + '}'


class WordNode(Node):
    def __init__(self,
                 identifier: str = None,
                 odour=None,
                 word: str = "",
                 target_lemma: str = ""):
        super().__init__(identifier, odour)
        if odour is None:
            odour = []
        self.word = word
        self.target_lemma = target_lemma

    def __repr__(self):
        return self.word


class NestNode(Node):
    def __init__(self,
                 identifier: str = None,
                 odour=None,
                 lemma: str = ""):
        super().__init__(identifier, odour)
        self.lemma = lemma



Edge = Set[Node]


class Graph:
    def __init__(self,
                 graph_dict: Dict[Node, List[Node]] = dict,
                 pheromones: Dict[Edge, float] = dict,
                 is_bridge: Dict[Edge, bool] = dict):
        self.root = Node()
        self.graph_dict = graph_dict
        self.pheromones = pheromones

    def get_edges(self, node: Node):
        dest_nodes = self.graph_dict.get(node)
        edges = [set(node, dest_node) for dest_node in dest_nodes]
        return edges

    def get_neighbours(self, node: Node):
        return self.graph_dict[node]

    def add_neighbour(self,node: Node,neighbour: Node):
        self.graph_dict[node].append(neighbour)

    def set_neighbours(self,node: Node,neighbours: List[Node]):
        self.graph_dict[node]=neighbours

    def get_pheromone(self, edge: Edge):
        if graph.pheromones.get(edge) is None:
            return 0
        return graph.pheromones.get(edge)

    def increment_pheromone(self, edge: Edge):
        if self.pheromones[edge] is None:
            self.pheromones[edge] = 1
        else:
            self.pheromones[edge] += 1

    def get_children(self,node:WordNode):
        return [child for child in self.get_neighbours(node) if isinstance(child, NestNode)]

    def get_parent(self,node:NestNode):
        return [parent for parent in self.get_neighbours(node) if isinstance(parent, WordNode)][0]




a, b, c, d, e = Node("a"), WordNode("b", word='mouse'), WordNode("c"), Node("d"), Node("e")

edges = {a: [b, c, d],
         b: [a],
         c: [a],
         d: [a]
         }

graph = Graph(graph_dict=edges)

# print(graph.edges)

for node in graph.graph_dict.keys():
    print(repr(node), graph.graph_dict.get(node))

print(hash('have'))

energy_list = np.array([1, 2, 3, 4, 5])
total_energy = sum(energy_list)
print(energy_list / total_energy)


node = Node(odour=np.array([1, 2, 3]))