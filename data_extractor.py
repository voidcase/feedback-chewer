import pandas as pd #using pandas.io (recommended in sklearn)
import numpy as np
import util
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import preprocessing

def data_extract():
    df = pd.read_csv('dataset.csv').drop(util.SCORE_TYPES + ['Proposal'], axis = 1)
    df = df.fillna('')

    for header in ['Beamline', 'Department', 'User Affiliation']:
        dummies = pd.get_dummies(df[header])
        df = pd.concat([df.drop([header], axis=1) ,dummies], axis = 1)

    for header, name in [('Experiment comments', '_ec'),
                         ('Infrastructure comment', '_ic'),
                         ('Overall comments', '_oc'),
                         ('Remarks', '_r')]:
        tfidf_frame = tfidf(df[header],name)
        df = pd.concat([df.drop([header], axis=1) , tfidf_frame], axis = 1)

    df['Experiment start'] = parse_date(df['Experiment start'])
    df['Experiment end'] = parse_date(df['Experiment end'])
    df['Report submitted'] = parse_date(df['Report submitted'])
    df_scaled = preprocessing.scale(df)
    return df_scaled

def tfidf(column, columname):
    values = column.values
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(values).toarray()
    featurenames = np.asarray(vectorizer.get_feature_names())
    tfidf_frame = pd.DataFrame(tfidf_matrix, columns=featurenames)
    tfidf_frame.rename(columns=lambda x: x+columname, inplace=True)
    return tfidf_frame

def parse_date(column):
    column = pd.to_datetime(column)
    column = [t.value // 10 ** 9 for t in column]
    return column
