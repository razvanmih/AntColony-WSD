import random
from typing import Dict, List, FrozenSet
import numpy as np
# import Ant
import utils


class Node:
    def __init__(self,
                 identifier: str = None,
                 energy: int = utils.NODE_STARTING_ENERGY):
        self.odour = np.zeros(utils.ODOUR_SIZE)
        self.identifier = str(identifier)
        self.energy = energy

    def __repr__(self):
        return '{id: ' + self.identifier + '}'

    def __str__(self):
        return '{id: ' + self.identifier + '}'


class WordNode(Node):
    def __init__(self,
                 identifier: str = None,
                 word: str = "",
                 ):
        super().__init__(identifier)
        self.word = word

    def __repr__(self):
        return '{id: ' + self.identifier + '|word: ' + self.word + '}'

    def __str__(self):
        return '{id: ' + self.identifier + '|word: ' + self.word + '}'


class NestNode(Node):
    def __init__(self,
                 identifier: str,
                 odour,
                 lemma: str = ""
                 ):
        super().__init__(identifier)
        self.odour = odour
        self.lemma = lemma

    def __repr__(self):
        return '{id: ' + self.identifier + '|lemma: ' + self.lemma + '}'

    def __str__(self):
        return '{id: ' + self.identifier + '|lemma: ' + self.lemma + '}'

    def generate_ant(self):
        if utils.ANT_START_ENERGY > self.energy:
            return
        if random.uniform(0, 1) <= np.arctan(self.energy) / np.pi + 0.5:
            self.energy -= utils.ANT_START_ENERGY
            return Ant(mother_nest=self,
                       odour=self.odour,
                       start_energy=utils.ANT_START_ENERGY,
                       max_energy=utils.ANT_MAX_ENERGY,
                       energy_pickup=utils.ANT_PICKUP_ENERGY)


Edge = FrozenSet[Node]


class Graph:
    def __init__(self,
                 root):
        self.root = root
        self.graph_dict: Dict[Node, List[Node]] = dict()
        self.pheromones: Dict[Edge, float] = dict()
        self.is_bridge: List[Edge] = []
        self.word_nodes: List[WordNode] = []
        self.nests: List[NestNode] = []

    def get_edges(self, node: Node):
        dest_nodes = self.graph_dict.get(node)
        edges = [set(node, dest_node) for dest_node in dest_nodes]
        return edges

    def get_pheromone_edges(self):
        return self.pheromones.keys()

    def get_neighbours(self, node: Node):
        return self.graph_dict[node]

    def add_neighbour(self, node: Node, neighbour: Node):
        if node in self.graph_dict.keys():
            self.graph_dict[node].append(neighbour)
        else:
            self.graph_dict[node] = [neighbour]
        if neighbour in self.graph_dict.keys():
            self.graph_dict[neighbour].append(node)
        else:
            self.graph_dict[neighbour] = [node]

    def set_neighbours(self, node: Node, neighbours: List[Node]):
        self.graph_dict[node] = neighbours

    def get_pheromone(self, edge: Edge):
        if edge not in self.pheromones.keys():
            return 0
        return self.pheromones.get(edge)

    def increment_pheromone(self, edge: Edge):
        if edge not in self.pheromones.keys():
            self.pheromones[edge] = utils.PHEROMONE_DEPOSIT
        else:
            self.pheromones[edge] += utils.PHEROMONE_DEPOSIT

    def get_children(self, node: WordNode):
        return [child for child in self.get_neighbours(node) if isinstance(child, NestNode)]

    def get_parent(self, node: NestNode):
        return [parent for parent in self.get_neighbours(node) if isinstance(parent, WordNode)][0]

    def create_or_reinforce_bridge(self, current_node, mother_nest):
        if mother_nest not in self.graph_dict[current_node]:
            self.add_neighbour(current_node, mother_nest)
        edge = frozenset({current_node, mother_nest})
        self.increment_pheromone(edge)
        if edge not in self.is_bridge:
            self.is_bridge.append(edge)

    def add_node(self, node, parent_node):
        self.add_neighbour(node, parent_node)

    def add_word_node(self, node, parent_node):
        self.add_neighbour(node, parent_node)
        self.word_nodes.append(node)

    def add_nest(self, node, parent_node):
        self.add_neighbour(node, parent_node)
        self.nests.append(node)

    def decrease_pheromone(self, edge):
        self.pheromones[edge] *= utils.PHEROMONE_RETENTION_RATE

    def remove_edge(self, edge):
        node1, node2 = edge
        self.drop_neighbours(node1, node2)
        del self.pheromones[edge]
        self.is_bridge.remove(edge)

    def drop_neighbours(self, node1, node2):
        # print(node1, self.graph_dict[node1])
        # print(node2, self.graph_dict[node2])
        # print("--")
        self.graph_dict[node1].remove(node2)
        self.graph_dict[node2].remove(node1)


class Ant:

    def __init__(self,
                 mother_nest: Node,
                 odour,
                 start_energy: int = 1,
                 max_energy: int = 5,
                 energy_pickup=1,
                 mode=utils.SEEK_ENERGY):

        self.mother_nest = mother_nest
        self.current_node = mother_nest
        self.energy = start_energy
        self.max_energy = max_energy
        self.energy_pickup = energy_pickup
        self.odour = odour
        self.mode = mode
        self.age = 0

    def choose_mode(self):
        if random.uniform(0, 1) < self.probability_to_flip_mode():
            self.mode = utils.GO_HOME

    def probability_to_flip_mode(self):
        return self.energy / self.max_energy

    def choose_node(self, graph: Graph):
        neighbours = graph.get_neighbours(self.current_node)
        neighbours = self.remove_enemy_nests(neighbours, graph)
        edges = [frozenset({self.current_node, node}) for node in neighbours]
        # print(str(self),"choosing neibour from ", neighbours)

        if self.mode == utils.SEEK_ENERGY:
            energy_list = np.array([node.energy for node in neighbours])
            pheromone_list = np.array([1 - graph.get_pheromone(edge) for edge in edges])
            pheromone_list = self.remove_pheromone_for_nests(neighbours, pheromone_list)
            eval_list = energy_list + pheromone_list

        else:
            similarity_list = np.array([utils.lesk_similarity(self.odour, neighbour.odour) for neighbour in neighbours])
            pheromone_list = np.array([graph.get_pheromone(edge) for edge in edges])
            pheromone_list = self.remove_pheromone_for_nests(neighbours, pheromone_list)
            eval_list = similarity_list + pheromone_list

        probabilities = eval_list / sum(eval_list)
        chosen_node = self.pick_node(neighbours, probabilities)
        # print(str(self),"chose node", chosen_node, "probabilities", probabilities,eval_list)

        return chosen_node

    def pick_node(self, neighbours, probabilities):
        r = random.random()
        for index, probability in enumerate(probabilities):
            if r <= probability:
                return neighbours[index]
            r -= probability

    def step(self, graph: Graph):
        self.age += 1

        if self.age > 1 and self.mode == utils.SEEK_ENERGY:
            self.choose_mode()

        target_node = self.choose_node(graph)
        target_edge = frozenset({self.current_node, target_node})

        graph.increment_pheromone(target_edge)
        self.current_node = target_node

        if self.current_node == self.mother_nest:
            self.deposit_energy()
            self.mode = utils.SEEK_ENERGY

        elif isinstance(self.current_node, NestNode):
            graph.create_or_reinforce_bridge(self.current_node, self.mother_nest)
            self.current_node = self.mother_nest
            self.deposit_energy()
            self.mode = utils.SEEK_ENERGY

        else:
            self.pickup_energy()
            self.deposit_odour()

        return target_node, target_edge

    def remove_enemy_nests(self, neighbours, graph):
        return [neighbour for neighbour in neighbours
                if neighbour not in graph.get_children(graph.get_parent(self.mother_nest))
                or neighbour == self.mother_nest]

    def remove_pheromone_for_nests(self, neighbours, pheromone_list):
        for index, node in enumerate(neighbours):
            if isinstance(node, NestNode):
                pheromone_list[index] = 0
        return pheromone_list

    def deposit_energy(self):
        self.current_node.energy += self.energy
        self.energy = 0

    def pickup_energy(self):
        if self.current_node.energy > self.energy_pickup:
            self.energy += self.energy_pickup
            self.current_node.energy -= self.energy_pickup
        else:
            self.energy += self.current_node.energy
            self.current_node.energy = 0

    def deposit_odour(self):
        for element in self.odour:
            r = random.uniform(0, 1)
            if r < utils.ODOUR_DEPOSIT:
                rand_index = random.randrange(self.current_node.odour.size)
                self.current_node.odour[rand_index] = element

    def kill(self):
        self.deposit_energy()

    def __repr__(self):
        return 'Ant|current node: ' + self.current_node.identifier

    def __str__(self):
        return 'Ant|current node: ' + self.current_node.identifier
        # + '|lemma: ' + self.lemma
