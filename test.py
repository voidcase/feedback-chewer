import data_extractor
import util
import os
import random
from sklearn import svm, ensemble
from pprint import pprint
import numpy as np
from sklearn.model_selection import train_test_split
import maxiv_data
from pprint import pprint

import score_predictor as sp

def test_dep_parse():
    print("DEPENDENCY PARSING")
    filename = "pickles/testcache.pickle"
    # data_extractor.dependency_parse("The cat is wearing boots", cache_file=filename))
    print("works without cache")
    # assert(data_extractor.dependency_parse("The cat is wearing boots", cache_file=filename))
    pprint(data_extractor.dependency_parse("The cat is wearing boots", cache_file=filename))
    print("works with cache")
    # assert(os.path.exists(filename))
    #assert (type(data_extractor.dependency_parse("The cat is wearing boots", cache_file=filename)) == dict)
    os.remove(filename)


def test_wordvec_parser():
    print('\nWORDVEC PARSER')
    word_vectors = data_extractor.parse_word_vectors(util.WORDVEC_DATA)
    the_vector = word_vectors['the']
    print('len:', len(the_vector))
    print('type:', type(the_vector))


def test_binarized_variance():
    df, y = data_extractor.data_extract_comments()
    print('number of 1\'s: ', len([i for i in y if i == 1]))
    print('number of 0\'s: ', len([i for i in y if i == 0]))

def test_cross_validation():
    cv_precisions = sp.cross_val()
    for label, scores in cv_precisions.items():
        print(label,'\n\t',scores)
    minscores = {label: min(scores) for label, scores in cv_precisions.items()}
    print('highest lowest:', max(minscores,key=minscores.get))

def test_across_datasets():
    scores = sp.cross_dataset_eval()
    print('training on Amazon, testing on Max IV:')
    for label, score in scores.items():
        print(label,':',score)


#to test if embeddings make sense
def test_closest_words():
    word_vectors = data_extractor.parse_word_vectors(util.WORDVEC_DATA)
    data_extractor.compute_closest_words(word_vectors, 'no', 10)


if __name__ == '__main__':
    sp.plot_cross_val()
    print('done!')