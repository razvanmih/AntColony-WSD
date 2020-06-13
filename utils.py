import numpy as np


def lesk_similarity(odour1: np.array, odour2: np.array):
    return np.intersect1d(odour1, odour2).shape[0]
