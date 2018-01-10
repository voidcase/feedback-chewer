import pandas as pd
import numpy as np
import util
import requests
import pickle
import os
import io
import autocorrect
# import gensim

def all_scores(df:pd.DataFrame) -> list:
    num_rows = df.shape[0]
    return [
        [df.iloc[i][t] for t in util.SCORE_TYPES]
        for i in range(num_rows)
    ]

def get_avg_target(df:pd.DataFrame) -> list:
    scores = all_scores(df)
    averages = [sum(s)/len(s) for s in scores]
    return averages

def get_lowest_target(df:pd.DataFrame) -> list:
    scores = all_scores(df)
    return [min(s) for s in scores]


def auto_correct(comments: list) -> list:
    try:
        cache = pickle.load(open(util.AUTOCORRECT_PICKLE_FILE, 'rb'))
        print("autocorrected words loaded from pickle")
        return cache
    except FileNotFoundError:
        corrected = [[autocorrect.spell(word) for word in comment] for comment in comments]
        pickle.dump(corrected, open(util.AUTOCORRECT_PICKLE_FILE, 'wb'))
        return corrected

def dependency_parse(comment, cache_file=util.VILDE_PICKLE_FILE):
    cache = {}
    try:
        cache = pickle.load(open(cache_file, 'rb'))
        if comment in cache:
            return cache[comment]
    except FileNotFoundError:
        if not os.path.exists('pickles/'):
            os.makedirs('pickles/')
    response = requests.post(url="http://vilde.cs.lth.se:9000/en/default/api/tsv", data=comment)
    response_frame = pd.read_csv(io.StringIO(response.text), sep='\t')
    cache[comment] = response_frame
    pickle.dump(cache, open(cache_file, 'wb'))
    return response_frame


def parse_word_vectors(filename:str) -> dict:
    try:
        cache = pickle.load(open(util.WORDVEC_PICKLE_FILE, 'rb'))
        print('word vectors loaded from pickle')
        return cache
    except FileNotFoundError:
        with open(filename, 'r', encoding='utf-8') as datafile:
            print('no pickled word vectors found, filtering original corpus, this might take a while...')
            #lines = [l for l in datafile][:100000]
            lines = [l for l in datafile if l.split()[0] in all_words]
            print('dbg: lines:', len(lines))
            vectors = {
                line.split()[0]:
                    np.array(normalize_vector([float(v) for v in line.split()[1:]]))
                    for line in lines
            }
            pickle.dump(vectors, open(util.WORDVEC_PICKLE_FILE, 'wb'))
            return vectors

def normalize_vector(vector:list) -> list:
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    else:
        return vector / norm

#to check if embeddings make sense
def compute_closest_words(vectors:dict, word, top:int) -> list:
    items = vectors.items()
    keys = [vect[0] for vect in items]
    index = keys.index(word)
    vectors = [vect[1] for vect in items]
    a = vectors[index]
    distances = [np.linalg.norm(a-b) for b in vectors]
    sorted_distances = sorted([(x,y) for x,y in enumerate(distances)], key=lambda x: x[1])
    closest = [keys[i] for i,j in sorted_distances[:top]]
    print(closest)

def json_dependency_parse(comment, cache_file=util.VILDE_PICKLE_FILE):
    cache = {}
    try:
        cache = pickle.load(open(cache_file, 'rb'))
        if comment in cache:
            return cache[comment]
    except FileNotFoundError:
        if not os.path.exists('pickles/'):
            os.makedirs('pickles/')
    response = requests.post(url="http://vilde.cs.lth.se:9000/en/default/api/json", data=comment).json()
    cache[comment] = response['DM10']
    pickle.dump(cache, open(cache_file, 'wb'))
    return response['DM10']

def get_txt_lineset(filename: str) -> set:
    with open(filename, 'r', encoding='utf-8') as datafile:
        return set(x.strip() for x in datafile)


#import gensim first
def create_word_embeddings(x:list) -> dict:
    try:
        cache = pickle.load(open(util.OWN_WORDVEC_PICKLE_FILE, 'rb'))
        print("own word vectors loaded from pickle")
        return cache
    except FileNotFoundError:
        print("no pickled words found, training word embeddings")
        model = gensim.models.Word2Vec(x, size=100)
        w2v_dict = dict(zip(model.wv.index2word, model.wv.syn0))
        pickle.dump(w2v_dict, open(util.OWN_WORDVEC_PICKLE_FILE, 'wb'))
        return w2v_dict