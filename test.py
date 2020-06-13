import random

import numpy as np
import nltk
from nltk.corpus import wordnet as wn
import utils
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

print(utils.lesk_similarity(odour1, odour2))


# syn = wn.synsets('monkey')[0]
#
# print(syn.lemmas()[0].key())


d = {("a","b"): "da"}

print(d[('a', 'b')])


a = GraphManager.Node()
b = GraphManager.Node()
l = [a,b]

for node in l:
    if isinstance(node, GraphManager.NestNode):
        print(node.lemma)

print(a==b)

