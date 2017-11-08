import pandas as pd
import numpy as np
import util
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import VarianceThreshold
from sklearn import preprocessing


def data_extract():
    df = pd.read_csv(util.DATASET).drop(util.DROPTEST, axis=1)
    df = df.fillna('')

    for header in util.NAME_HEADERS:
        if header in df:
            dummies = pd.get_dummies(df[header])
            df = pd.concat([df.drop([header], axis=1), dummies], axis=1)

    #supercomment!
    df['supercomment'] = ""
    for header in util.TEXT_HEADERS:
        if header in df:
            df['supercomment'] += df[header]
    values = df['supercomment'].values
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(values).toarray()
    featurenames = np.asarray(vectorizer.get_feature_names())
    tfidf_frame = pd.DataFrame(tfidf_matrix, columns=featurenames)
    df = df.drop(util.TEXT_HEADERS + ['supercomment'], axis=1)
    df = pd.concat([df, tfidf_frame], axis=1)

    # for header, suffix in util.TEXT_HEADERS_AND_SUFFIXES:
    #     if header in df:
    #         tfidf_frame = tfidf(df[header], suffix)
    #         df = pd.concat([df.drop([header], axis=1), tfidf_frame], axis=1)

    for header in util.DATE_HEADERS:
        if header in df:
            df[header] = parse_date(df[header])

    min_max_scaler = preprocessing.MinMaxScaler()
    variance_scaler = VarianceThreshold(0.001)

    kept_dates = list(set(util.DATE_HEADERS) - set(util.DROPTEST))
    if kept_dates:
        df[kept_dates] = min_max_scaler.fit_transform(df[kept_dates])
    variance_scaler.fit(df)

    retain = variance_scaler.get_support()
    droppable_headers = [df.columns[x] for x, y in enumerate(retain) if not y]
    df = df.drop(droppable_headers, axis=1)
    # df = df.iloc[:, lambda df: retain_indices]
    print("df after drops:",df.columns)
    return df

def get_all_data():
    df = pd.read_csv(util.DATASET)
    return df

def getXandY(y='Overall'):
    y_col = get_all_data()[y]
    x = data_extract()
    return x, y_col

def tfidf(column, columname):
    values = column.values
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(values).toarray()
    featurenames = np.asarray(vectorizer.get_feature_names())
    tfidf_frame = pd.DataFrame(tfidf_matrix, columns=featurenames)
    tfidf_frame.rename(columns=lambda x: x + columname, inplace=True)
    return tfidf_frame


def parse_date(column):
    column = pd.to_datetime(column)
    column = [t.value // 10 ** 9 for t in column]
    return column
