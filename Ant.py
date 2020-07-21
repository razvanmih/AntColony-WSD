# import random
# import numpy as np
# import utils
# import GraphManager
#
#
# class Ant:
#
#     def __init__(self,
#                  mother_nest: GraphManager.Node,
#                  odour,
#                  start_energy: int = 1,
#                  max_energy: int = 5,
#                  energy_pickup=1,
#                  mode=utils.SEEK_ENERGY):
#
#         self.mother_nest = mother_nest
#         self.current_node = mother_nest
#         self.energy = start_energy
#         self.max_energy = max_energy
#         self.energy_pickup = energy_pickup
#         self.odour = odour
#         self.mode = mode
#         self.age = 0
#
#     def choose_mode(self):
#         if random.uniform(0, 1) > self.probability_to_flip_mode():
#             self.mode = utils.GO_HOME
#
#     def probability_to_flip_mode(self):
#         return self.energy / self.max_energy
#
#     def choose_node(self, graph: GraphManager.Graph):
#         neighbours = graph.get_neighbours(self.current_node)
#         neighbours = self.remove_enemy_nests(neighbours)
#         edges = [{self.current_node, node} for node in neighbours]
#
#         if self.mode == utils.SEEK_ENERGY:
#             energy_list = np.array([node.energy for node in neighbours])
#             pheromone_list = np.array([1 - graph.get_pheromone(edge) for edge in edges])
#             pheromone_list = self.remove_pheromone_for_nests(neighbours, pheromone_list)
#             eval_list = energy_list + pheromone_list
#
#         else:
#             similarity_list = np.array([utils.lesk_similarity()])
#             pheromone_list = np.array([graph.get_pheromone(edge) for edge in edges])
#             pheromone_list = self.remove_pheromone_for_nests(neighbours, pheromone_list)
#             eval_list = similarity_list + pheromone_list
#
#         probabilities = eval_list / sum(eval_list)
#         return self.pick_node(neighbours, probabilities)
#
#     def pick_node(self, neighbours, probabilities):
#         r = random.uniform(0, 1)
#         for index, probability in enumerate(probabilities):
#             if r <= probability:
#                 return neighbours[index]
#             r -= probability
#
#     def step(self, graph: GraphManager.Graph):
#         self.age += 1
#
#         if self.mode == utils.SEEK_ENERGY:
#             self.choose_mode()
#
#         target_node = self.choose_node(graph)
#         target_edge = {self.current_node, target_node}
#
#         graph.increment_pheromone(target_edge)
#         self.current_node = target_node
#
#         if self.current_node == self.mother_nest:
#             self.deposit_energy()
#             self.mode = utils.SEEK_ENERGY
#
#         elif isinstance(self.current_node, GraphManager.NestNode):
#             graph.create_or_reinforce_bridge(self.current_node, self.mother_nest)
#             self.current_node = self.mother_nest
#             self.deposit_energy()
#             self.mode = utils.SEEK_ENERGY
#
#         else:
#             self.pickup_energy()
#             self.deposit_odour()
#
#         return target_node, target_edge
#
#     def remove_enemy_nests(self, neighbours, graph):
#         return [neighbour for neighbour in neighbours
#                 if neighbour not in graph.get_children(graph.get_parent(self.mother_nest))
#                 or neighbour == self.mother_nest]
#
#     def remove_pheromone_for_nests(self, neighbours, pheromone_list):
#         for index, node in enumerate(neighbours):
#             if isinstance(node, GraphManager.NestNode):
#                 pheromone_list[index] = 0
#         return pheromone_list
#
#     def deposit_energy(self):
#         self.current_node.energy += self.energy
#         self.energy = 0
#
#     def pickup_energy(self):
#         if self.current_node.energy > self.energy_pickup:
#             self.energy += self.energy_pickup
#             self.current_node.energy -= self.energy_pickup
#         else:
#             self.energy += self.current_node.energy
#             self.current_node.energy = 0
#
#     def deposit_odour(self):
#         for element in self.odour:
#             r = random.uniform(0, 1)
#             if r < self.odour_deposit_rate:
#                 rand_index = random.randrange(self.current_node.odour.size)
#                 self.current_node.odour[rand_index] = element
#
#     def kill(self):
#         self.deposit_energy()
