import data_extractor
import util
import os

def test_dep_parse():
    print("DEPENDENCY PARSING")
    filename = "pickles/testcache.pickle"
    assert(data_extractor.dependency_parse("The cat is wearing boots", cache_file=filename))
    print("works without cache")
    assert(data_extractor.dependency_parse("The cat is wearing boots", cache_file=filename))
    print(data_extractor.dependency_parse("The cat is wearing boots", cache_file=filename))
    print("works with cache")
    assert(os.path.exists(filename))
    os.remove(filename)



if __name__ == '__main__':
    test_dep_parse()
    print('done!')