import data_extractor
import util
import os
import random
from pprint import pprint
from sklearn.model_selection import train_test_split

import score_predictor as sp

def test_dep_parse():
    print("DEPENDENCY PARSING")
    filename = "pickles/testcache.pickle"
    assert(data_extractor.dependency_parse("The cat is wearing boots", cache_file=filename))
    print("works without cache")
    assert(data_extractor.dependency_parse("The cat is wearing boots", cache_file=filename))
    pprint(data_extractor.dependency_parse("The cat is wearing boots", cache_file=filename))
    print("works with cache")
    assert(os.path.exists(filename))
    assert (type(data_extractor.dependency_parse("The cat is wearing boots", cache_file=filename)) == dict)
    os.remove(filename)


def test_sentimenter():
    print('\nSENTIMENTER')
    #annotated = ws.sentiment_annotate('We had problems with very low intensity all afternoon, but the food was nice')
    #print(annotated)

def test_wordvec_parser():
    print('\nWORDVEC PARSER')
    word_vectors = data_extractor.parse_word_vectors(util.WORDVEC_DATA)
    print(word_vectors)
    the_vector = word_vectors['the']
    print(the_vector)
    print('len:', len(the_vector))
    print('type:', type(the_vector))

def test_avg():
    print(data_extractor.get_avg_target(data_extractor.get_all_data()))

def test_binarized_variance():
    df, y = data_extractor.data_extract_comments()
    print('number of 1\'s: ', len([i for i in y if i == 1]))
    print('number of 0\'s: ', len([i for i in y if i == 0]))

def test_cross_validation():
    cv_precisions = sp.cross_validate()
    for label, scores in cv_precisions.items():
        print(label,'\n\t',scores)
    minscores = {label: min(scores) for label, scores in cv_precisions.items()}
    print('highest lowest:', max(minscores,key=minscores.get))

def test_print_example_predictions():
    x, y = data_extractor.data_extract_comments()

    #non_empties = [comment for comment in x['supercomment'] if comment != []]
    models = sp.make_models(w2v=True)
    x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.05)
    for label, model in models.items():
        model.fit(x_train, y_train)
    print(x_test.head(3))
    for label, model in models.items():
        print(label, ':', model.predict(x_test.head(3)))

if __name__ == '__main__':
    test_cross_validation()
    print('done!')