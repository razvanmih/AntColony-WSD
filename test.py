import random

import numpy as np
import utils
import FileReader
import GraphManager

energy_list = np.array([5, 2, 3, 4, 5])
pheromone_list = np.array([0, 1, .5, .5, .5])
eval_list = energy_list + pheromone_list
probabilities = eval_list / sum(eval_list)

print(sum(eval_list))
print(probabilities)


def pick_node(probabilities):
    r = random.uniform(0, 1)
    print(r)
    for index, probability in enumerate(probabilities):
        if r <= probability:
            return index
        r -= probability


print(pick_node(probabilities))

odour1 = np.array([1, 2, 3, 4, 5])
odour2 = np.array([3, 5, 7, 8, 9, 1])

print("SIZE", odour2.size)

print(utils.lesk_similarity(odour1, odour2))

# syn = wn.synsets('monkey')[0]
#
# print(syn.lemmas()[0].key())


d = {("a", "b"): "da"}

print(d[('a', 'b')])

a = GraphManager.Node()
b = GraphManager.Node()
l = [a, b]

for node in l:
    if isinstance(node, GraphManager.NestNode):
        print(node.lemma)

print(set([a, b]) == set([b, a]))

print(str(None))

parser = FileReader.SemEvalParser()

sent_ids = parser.get_sentences_ids_by('d001')
sent = parser.get_instances_by(sentence=sent_ids[0])
print(sent_ids)
print(sent)

# a, b, c, d, e = Node("a"), WordNode("b", word='mouse'), WordNode("c"), Node("d"), Node("e")
#
# edges = {a: [b, c, d],
#          b: [a],
#          c: [a],
#          d: [a]
#          }
#
# graph = Graph(graph_dict=edges)
#
# # print(graph.edges)
#
# for node in graph.graph_dict.keys():
#     print(repr(node), graph.graph_dict.get(node))
#
# print(hash('have'))
#
# energy_list = np.array([1, 2, 3, 4, 5])
# total_energy = sum(energy_list)
# print(energy_list / total_energy)
#
#
# node = Node(odour=np.array([1, 2, 3]))
x = 1
for i in range(100):
    x *= .8

print(x == 0)

vocabulary = dict()
index = 1


def get_index(word):
    global index
    index += 1


print(index)
get_index("word")
print(index)
get_index("word")

print(frozenset({'a', 'b'}) == frozenset({'b', 'a'}))
print(np.array([1,2])+np.array([3,4]))
a, b = frozenset({'ana are mere','babuin'})

print(a,b)