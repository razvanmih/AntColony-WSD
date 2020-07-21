import numpy as np
from nltk.corpus import wordnet as wn
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

NODE_STARTING_ENERGY = 30

ANT_START_ENERGY = 1
ANT_MAX_ENERGY = 20
ANT_PICKUP_ENERGY = 16
ANT_MAX_AGE = 56
ODOUR_DEPOSIT = .975
ODOUR_SIZE = 50

PHEROMONE_DEPOSIT = 1
PHEROMONE_RETENTION_RATE = .9

EPSILON = 1e-4
SEEK_ENERGY = 0
GO_HOME = 1


def lesk_similarity(odour1: np.array, odour2: np.array):
    return np.intersect1d(odour1, odour2).shape[0]


tokenizer = RegexpTokenizer(r'\w+')
ps = SnowballStemmer("english")


def get_all_related_synsets(synset):
    relations = set()
    relations.update(synset.hypernyms())
    relations.update(synset.hyponyms())
    relations.update(synset.substance_meronyms())
    relations.update(synset.part_meronyms())
    relations.update(synset.member_meronyms())
    relations.update(synset.substance_holonyms())
    relations.update(synset.part_holonyms())
    relations.update(synset.member_holonyms())
    relations.update(synset.attributes())
    relations.update(synset.also_sees())
    relations.update(synset.similar_tos())
    return relations


def get_extended_def(syn1):
    extended_definition = syn1.definition()
    for syn in get_all_related_synsets(syn1):
        extended_definition += syn.definition()
    extended_definition = tokenizer.tokenize(extended_definition)
    extended_definition = [word for word in extended_definition if word not in stopwords.words('english')]
    # stemming
    extended_definition = [ps.stem(word) for word in extended_definition]
    # eliminate duplicates
    return set(extended_definition)


def get_sences(word):
    return wn.synsets(word)