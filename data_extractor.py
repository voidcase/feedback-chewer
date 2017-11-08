import pandas as pd
import numpy as np
import util
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import VarianceThreshold
from sklearn import preprocessing



def data_extract():
    df = pd.read_csv(util.DATASET).drop(util.SCORE_TYPES + ['Proposal'], axis=1)
    df = df.fillna('')

    for header in util.NAME_HEADERS:
        dummies = pd.get_dummies(df[header])
        df = pd.concat([df.drop([header], axis=1), dummies], axis=1)

    for header, suffix in util.TEXT_HEADERS_AND_SUFFIXES:
        tfidf_frame = tfidf(df[header], suffix)
        df = pd.concat([df.drop([header], axis=1), tfidf_frame], axis=1)

    dates = util.DATE_HEADERS
    for header in dates:
        df[header] = parse_date(df[header])

    min_max_scaler = preprocessing.MinMaxScaler()
    variance_scaler = VarianceThreshold(0.005)
    df[dates] = min_max_scaler.fit_transform(df[dates])
    variance_scaler.fit(df)

    retain = variance_scaler.get_support()
    retain_indices = [x for x in range(len(retain)) if retain[x]]
    #for i in remove_indices:
        #print('dropped', df.columns[i])
     #   df.drop(df.columns[i], axis=1)
    df = df.iloc[:, lambda df: retain_indices]
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

