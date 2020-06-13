from typing import Dict, Tuple, List, Set
import random
import numpy as np

import utils
from GraphManager import Node, Edge, Graph, NestNode,WordNode

SEEK_ENERGY = 0
GO_HOME = 1


class Ant:

    def __init__(self,
                 mother_nest: Node,
                 current_node: Node,
                 odour,
                 start_energy: int = 1,
                 max_energy: int = 5,
                 mode=SEEK_ENERGY):
        self.mother_nest = mother_nest
        self.current_node = current_node
        self.energy = start_energy
        self.max_energy = max_energy
        self.odour = odour
        self.mode = mode

    def choose_mode(self):
        if random.uniform(0, 1) > self.probability_to_flip_mode():
            self.mode = GO_HOME

    def probability_to_flip_mode(self):
        return self.energy / self.max_energy

    def choose_node(self, graph: Graph):
        neighbours = graph.get_neighbours(self.current_node)
        neighbours = self.remove_enemy_nests(neighbours)
        edges = [(self.current_node, node) for node in neighbours]

        if self.mode == SEEK_ENERGY:
            energy_list = np.array([node.energy for node in neighbours])
            pheromone_list = np.array([1 - graph.get_pheromone(edge) for edge in edges])
            pheromone_list = self.remove_pheromone_for_nests(neighbours,pheromone_list)
            eval_list = energy_list + pheromone_list

        else:
            similarity_list = np.array([utils.lesk_similarity()])
            pheromone_list = np.array([graph.get_pheromone(edge) for edge in edges])
            pheromone_list = self.remove_pheromone_for_nests(neighbours, pheromone_list)
            eval_list = similarity_list + pheromone_list

        probabilities = eval_list / sum(eval_list)
        return self.pick_node(neighbours, probabilities)

    def pick_node(self, neighbours, probabilities):
        r = random.uniform(0, 1)
        for index, probability in enumerate(probabilities):
            if r <= probability:
                return neighbours[index]
            r -= probability

    def step(self, graph):
        if self.mode == SEEK_ENERGY:
            self.choose_mode()

        target_node = self.choose_node(graph)
        target_edge = (self.current_node, target_node)

        return target_node, target_edge

    def remove_enemy_nests(self, neighbours, graph):
        return [neighbour for neighbour in neighbours
                if neighbour not in graph.get_children(graph.get_parent(self.mother_nest))]

    def remove_pheromone_for_nests(self,neighbours, pheromone_list):
        for index , node in enumerate(neighbours):
            if isinstance(node, NestNode):
                pheromone_list[index] = 0
        return pheromone_list
