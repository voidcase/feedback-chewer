import pandas as pd
import numpy as np
import util
import requests
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.feature_selection import VarianceThreshold
from sklearn import preprocessing


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
    #   vectorizer = CountVectorizer(stop_words='english', min_df=util.MIN_DF)
    #   matrix = vectorizer.fit_transform(values).toarray()
    featurenames = np.asarray(vectorizer.get_feature_names())
    tfidf_frame = pd.DataFrame(tfidf_matrix, columns=featurenames)
    #   tf_frame = pd.DataFrame(matrix, columns=featurenames)
    df = df.drop(util.TEXT_HEADERS + ['supercomment'], axis=1)
    df = pd.concat([df, tfidf_frame], axis=1)
    #   df = pd.concat([df, tf_frame], axis=1)
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
