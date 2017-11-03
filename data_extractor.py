import pandas as pd #using pandas.io (recommended in sklearn)
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def parse_date(column):
    column = pd.to_datetime(column)
    column = [t.value // 10 ** 9 for t in column]
    return column

def data_extract():
    df = pd.read_csv('dataset.csv').drop(['Proposal'], axis = 1)
    df = df.fillna('')

    for header in ['Beamline', 'Department', 'User Affiliation']:
        dummies = pd.get_dummies(df[header])
        df = pd.concat([df.drop([header], axis=1) ,dummies], axis = 1)

    df['Experiment start'] = parse_date(df['Experiment start'])
    df['Experiment end'] = parse_date(df['Experiment end'])
    df['Report submitted'] = parse_date(df['Report submitted'])
    return df

def tfidf(column):
    values = column.values
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(values).toarray()
    featurenames = np.asarray(vectorizer.get_feature_names())
    tfidf_frame = pd.DataFrame(tfidf_matrix, columns=featurenames)
    return tfidf_frame

#df = pd.concat([df.drop(['Experiment comments'], axis=1) ,tfidf(df['Experiment comments'])], axis = 1)

#tfidf_matrix = vectorizer.fit_transform(df['Experiment comments'])

print(df.head())










