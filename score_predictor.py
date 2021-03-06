from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score, cross_val_predict, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.metrics import accuracy_score, f1_score
import numpy as np
import pandas as pd
import csv
from pandas_ml import ConfusionMatrix
from data_extractor import dependency_parse
import matplotlib.pyplot as plt
import maxiv_data, amazon_data
import transforms as tf

def make_models() -> dict:
    classifiers = [
        ("logistic regression", LogisticRegression()),
        ("GaussianNB", GaussianNB()),
        ("extra trees", ExtraTreesClassifier(n_estimators=150)),
        ("random forest", RandomForestClassifier(n_estimators=200)),
        ("svm", svm.SVC())
    ]

    return {
        label : Pipeline([(label, clf)])
        for label, clf in classifiers
    }

def get_xy(model:pd.DataFrame) -> (pd.DataFrame, pd.Series):
    x = model.drop([h for h in model if h in ['text','tokens','score']], axis=1)
    y = model['score']
    return x,y

def apply_transforms(df:pd.DataFrame,transforms:list) -> pd.DataFrame:
    for label, transform in [
        ('tokenizing',tf.token_transform),
        ('binarizing',tf.binarize_transform),
        ('tfidf', tf.tfidf_transform),
        ('autocorrecting',tf.auto_correct_transform),
        ('embedding',tf.embedding_transform)
    ]:
        if label in transforms:
            df = transform(df)
    return df

def cross_val(scoring = 'f1'):
    with open('plots/real_amazon_f1scores.csv', 'w') as csvfile:
        fieldnames = ['classifier', 'tfidf', 'embedding','tfidf+embedding']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        models = make_models()
        for label, model in models.items():
            modeldict = {'classifier':label}
            for transformlabel, transforms in [ ('tfidf', ['tfidf']),
                                                ('embedding',['embedding']),
                                                ('tfidf+embedding', ['tfidf', 'embedding'])]:
                df = amazon_data.get_set()
                df = apply_transforms(df,['autocorrect','tokenizing','binarizing'] + transforms)
                x, y = get_xy(df)
                modeldict[transformlabel] = np.mean(cross_val_score(model, x, y, scoring='f1'))
            writer.writerow(modeldict)
            print(modeldict)

def cm_cross_val():
    for label, transforms in [('tfidf', ['tfidf']),
                              ('embedding',['embedding']),
                              ('tfidf_embedding', ['tfidf', 'embedding'])
                              ]:
        df = amazon_data.get_set()
        df = apply_transforms(df,['tokenizing', 'binarizing'] + transforms)
        x, y = get_xy(df)
        lr = LogisticRegression()
        predicted = cross_val_predict(lr,x,y)
        confusion_matrix = ConfusionMatrix(y, predicted)
        print('confusion matrix:', confusion_matrix)
        confusion_matrix.plot()
        plt.show()

# used by server
def get_coeffs(types=['adverbs','adjectives', 'verbs', 'nouns']):
    df = maxiv_data.get_split_set()
    df = apply_transforms(df,['tokenizing', 'autocorrect', 'binarizing', 'tfidf'])
    x, y = get_xy(df)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33)
    lr = LogisticRegression()
    lr.fit(x_train, y_train)
    tups = list(zip(lr.coef_[0], list(x)))
    filtered_tups = filter(lambda x : typefilter(types, x[1]), tups)
    return sorted(list(filtered_tups))

# used by server
def typefilter(types:list, string):
    dict = {'adverbs': 'ADV', 'adjectives': 'ADJ', 'verbs': 'VERB', 'nouns': 'NOUN'}
    postags = [dict[type] for type in types]
    df = dependency_parse(string)
    for index, row in df.iterrows():
        if row['cpostag'] in postags: return True
    return False

if __name__ == '__main__':
    cm_cross_val() # calculate confusion matrix (Logistic regression, can be changed)
    cross_val('f1') # cross validate all models, generate csv file with scores