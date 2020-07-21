import FileReader
import utils
import GraphManager
import numpy as np

doc_id = 'd001'
cycles = 100

vocabulary = dict()
index = 1


def get_index(word):
    global index
    if word not in vocabulary.keys():
        vocabulary[word] = index
        index += 1
    return vocabulary[word]


def convert_extended_def_to_odour(definition):
    odour = []
    for word in definition:
        odour.append(get_index(word))

    return np.array(odour)


def create_graph():
    parser = FileReader.SemEvalParser()
    sent_ids = parser.get_sentences_ids_by(doc_id)
    root = GraphManager.Node(doc_id)
    graph = GraphManager.Graph(root=root)

    # sent_ids = sent_ids[:2]

    for sent_id in sent_ids:
        sent_node = GraphManager.Node(sent_id)
        graph.add_node(sent_node, root)

        words = parser.get_instances_by(sentence=sent_id)
        for node_id, word in words:
            word_node = GraphManager.WordNode(identifier=node_id, word=word)
            graph.add_word_node(word_node, sent_node)

            senses = utils.get_sences(word)
            for sense in senses:
                extended_def = utils.get_extended_def(sense)
                odour = convert_extended_def_to_odour(extended_def)
                nest = GraphManager.NestNode(identifier=sense,
                                             lemma=sense.lemmas()[0].key(),
                                             odour=odour)
                graph.add_nest(nest, word_node)
    global vocabulary
    global index
    del vocabulary
    del index
    return graph


def eliminate_ants():
    for ant in ants:
        if ant.age >= utils.ANT_MAX_AGE:
            ant.kill()
            ants.remove(ant)


def generate_ants():
    for nest in graph.nests:
        ant = nest.generate_ant()
        if ant:
            ants.append(ant)


def move_ants():
    return [ant.step(graph) for ant in ants]


def decrease_pheromone():
    for edge in graph.get_pheromone_edges():
        graph.decrease_pheromone(edge)


def break_bridges():
    for bridge in graph.is_bridge:
        if graph.get_pheromone(bridge) < utils.EPSILON:
            graph.remove_edge(bridge)


def update_environment():
    # node energy level adjusted during ant movement
    # edge pheromone level increased during ant movement
    # bridge creation done doring ant movement
    decrease_pheromone()
    break_bridges()


if __name__ == "__main__":
    ants = []
    graph = create_graph()

    # print(len(graph.word_nodes))
    # print(graph.word_nodes)
    # print(graph.nests[1])
    # print(len(graph.nests))

    for cycle in range(1, cycles + 1):
        #print(cycle)
        eliminate_ants()
        generate_ants()
        move_ants()
        update_environment()
        if cycle % 20 == 0:
            file_name = doc_id + "_answers_cycle_" + str(cycle) + ".txt"
            file = open(file_name, 'w')
            print("saving to file:" + file_name)
            for word in graph.word_nodes:
                energy_list = [node.energy for node in graph.get_children(word)]
                if energy_list:
                    sense_index = np.argmax(energy_list)
                    file.write(doc_id + " " + word.identifier + " "
                               + graph.get_children(word)[sense_index].lemma + "\n")
            file.close()

    # print(ants)
    # print(len(ants))
    # print(graph.is_bridge)

