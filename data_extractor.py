import pandas as pd
import numpy as np
import util
import requests
import pickle
import os
import random
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.feature_selection import VarianceThreshold
from sklearn import preprocessing
import autocorrect
import wordset
import gensim
from scipy.spatial.distance import cdist
import json

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



def data_extract_comments(config=util.DEFAULT_CONFIG):
    df = pd.read_csv(util.FEEDBACK_DATA)[util.TEXT_HEADERS + util.SCORE_TYPES]
    #df = df.dropna(subset=util.TEXT_HEADERS, how='all')
    df = df.fillna('')
    df = df.drop(df[df['Overall'] == 0].index)
    df['supercomment'] = ""
    for header in util.TEXT_HEADERS:
        df['supercomment'] += df[header]
    df = df.drop(util.TEXT_HEADERS, axis=1)
    df['supercomment'] = [split_text(comment) for comment in df['supercomment']]
    # print(df['supercomment'])
    y = binarize_scores(get_avg_target(df))
    df = df.drop(util.SCORE_TYPES, axis=1)
    return df, y

def data_extract_tfidf_comments(config=util.DEFAULT_CONFIG):
    df = data_extract_comments(config)[0]
    values = df['supercomment'].values
    vectorizer = TfidfVectorizer(stop_words=None, analyzer=lambda x: x)
    tfidf_matrix = vectorizer.fit_transform(values).toarray()
    return tfidf_matrix

def data_extract(config: dict = util.DEFAULT_CONFIG) -> pd.DataFrame:
    df = pd.read_csv(util.FEEDBACK_DATA).drop(util.DROPTEST, axis=1)
    df = df.fillna('')

    for header in util.NAME_HEADERS:
        if header in df:
            dummies = pd.get_dummies(df[header])
            df = pd.concat([df.drop([header], axis=1), dummies], axis=1)

    df = supercomment(df)
    # df = sep_comments(df)

    for header in util.DATE_HEADERS:
        if header in df:
            df[header] = parse_date(df[header])

    min_max_scaler = preprocessing.MinMaxScaler()
    variance_scaler = VarianceThreshold(config['variance_threshold'])

    kept_dates = list(set(util.DATE_HEADERS) - set(config['droplist']))
    if kept_dates:
        df[kept_dates] = min_max_scaler.fit_transform(df[kept_dates])
    variance_scaler.fit(df)

    retain = variance_scaler.get_support()
    droppable_headers = [df.columns[x] for x, y in enumerate(retain) if not y]
    df = df.drop(droppable_headers, axis=1)
    return df

def auto_correct(comments: list) -> list:
    try:
        cache = pickle.load(open(util.AUTOCORRECT_PICKLE_FILE, 'rb'))
        print("autocorrected words loaded from pickle")
        return cache
    except FileNotFoundError:
        corrected = [[autocorrect.spell(word) for word in comment] for comment in comments]
        pickle.dump(corrected, open(util.AUTOCORRECT_PICKLE_FILE, 'wb'))
        return corrected

def sep_comments(df: pd.DataFrame):
    for header, suffix in util.TEXT_HEADERS_AND_SUFFIXES:
        if header in df:
            tfidf_frame = tfidf_sep_comments(df[header], suffix)
            df = pd.concat([df.drop([header], axis=1), tfidf_frame], axis=1)
    return df


def get_x_and_y(config=util.DEFAULT_CONFIG) -> (pd.DataFrame, list):
    y_col = get_all_data()['Overall']
    x = data_extract(config)
    return x, y_col


def supercomment(df: pd.DataFrame):
    df['supercomment'] = ""
    for header in util.TEXT_HEADERS:
        if header in df:
            df['supercomment'] += df[header]
    values = df['supercomment'].values
    vectorizer = TfidfVectorizer(stop_words='english', min_df=util.MIN_DF)
    tfidf_matrix = vectorizer.fit_transform(values).toarray()
    featurenames = np.asarray(vectorizer.get_feature_names())
    tfidf_frame = pd.DataFrame(tfidf_matrix, columns=featurenames)
    df = df.drop(util.TEXT_HEADERS + ['supercomment'], axis=1)
    df = pd.concat([df, tfidf_frame], axis=1)
    return df


def tfidf_sep_comments(column, columname):
    values = column.values
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(values).toarray()
    featurenames = np.asarray(vectorizer.get_feature_names())
    tfidf_frame = pd.DataFrame(tfidf_matrix, columns=featurenames)
    tfidf_frame.rename(columns=lambda x: x + columname, inplace=True)
    return tfidf_frame


def get_all_data() -> pd.DataFrame:
    df = pd.read_csv(util.FEEDBACK_DATA)
    df = df.fillna('')
    return df


def parse_date(column):
    column = pd.to_datetime(column)
    column = [t.value // 10 ** 9 for t in column]
    return column


def dependency_parse(comment, cache_file=util.VILDE_PICKLE_FILE):
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


def parse_word_vectors(filename:str) -> dict:
    try:
        cache = pickle.load(open(util.WORDVEC_PICKLE_FILE, 'rb'))
        print('word vectors loaded from pickle')
        return cache
    except FileNotFoundError:
        with open(filename, 'r', encoding='utf-8') as datafile:
            print('no pickled word vectors found, filtering original corpus, this might take a while...')
            lines = [l for l in datafile][:1000000]
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


def binarize_scores(y:list) -> list:
    return [
        1 if score > 3
            else 0 # if score < 3
            # else random.randint(0,1) # score == 3
        for score in y
    ]

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