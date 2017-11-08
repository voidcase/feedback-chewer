import pandas as pd
import numpy as np
import util
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import VarianceThreshold
from sklearn import preprocessing


def data_extract():
    df = pd.read_csv('dataset.csv').drop(util.DROPTEST, axis=1)
    df = df.fillna('')

    for header in util.NAME_HEADERS:
        if header in df:
            dummies = pd.get_dummies(df[header])
            df = pd.concat([df.drop([header], axis=1), dummies], axis=1)

    for header, suffix in util.TEXT_HEADERS_AND_SUFFIXES:
        if header in df:
            tfidf_frame = tfidf(df[header], suffix)
            df = pd.concat([df.drop([header], axis=1), tfidf_frame], axis=1)

    for header in util.DATE_HEADERS:
        if header in df:
            df[header] = parse_date(df[header])

    min_max_scaler = preprocessing.MinMaxScaler()
    variance_scaler = VarianceThreshold(0.005)

    kept_dates = list(set(util.DATE_HEADERS) - set(util.DROPTEST))
    if kept_dates:
        df[kept_dates] = min_max_scaler.fit_transform(df[kept_dates])
    variance_scaler.fit(df)

    remove = variance_scaler.get_support()
    remove_indices = [x for x in range(len(remove)) if remove[x]]
    for i in remove_indices:
        print('dropped', df.columns[i])
        df.drop(df.columns[i], axis=1)
    #df = df.iloc[:, lambda df: remove_indices]
    return df


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
