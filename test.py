import data_extractor
import util
import os
import word_sentimenter as ws
from pprint import pprint

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
    annotated = ws.sentiment_annotate('We had problems with very low intensity all afternoon, but the food was nice')
    print(annotated)


if __name__ == '__main__':
    test_dep_parse()
    test_sentimenter()
    print('done!')