import util
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score, cross_validate, cross_val_predict, train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
import plotly.plotly as py
import plotly.graph_objs as go
from pandas_ml import ConfusionMatrix
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.metrics import accuracy_score, f1_score
from embedding_vectorizer import EmbeddingVectorizer
from data_extractor import data_extract_comments, parse_word_vectors, data_extract_tfidf_comments, create_word_embeddings
from sklearn.metrics import confusion_matrix, make_scorer
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
import maxiv_data
import amazon_data
import transforms as tf
from collections import defaultdict
from pprint import pprint

def tp(y_true, y_pred): return confusion_matrix(y_true, y_pred)[1, 1]
def tn(y_true, y_pred): return confusion_matrix(y_true, y_pred)[0, 0]
def fp(y_true, y_pred): return confusion_matrix(y_true, y_pred)[0, 1]
def fn(y_true, y_pred): return confusion_matrix(y_true, y_pred)[1, 0]

def cm(model, x, y) -> list:
    scoring = {'tp': make_scorer(tp), 'tn': make_scorer(tn), 'fp': make_scorer(fp), 'fn': make_scorer(fn)}
    cv = cross_validate(model.fit(x,y), x, y, scoring=scoring)
    mean_tp = round(np.mean(cv['test_tp']))
    mean_fp = round(np.mean(cv['test_fp']))
    mean_tn = round(np.mean(cv['test_tn']))
    mean_fn = round(np.mean(cv['test_fn']))
    print(mean_tn, mean_fp, mean_tp, mean_fn)
    df_cm = pd.DataFrame([[mean_tn, mean_fn], [mean_fp, mean_tp]], range(2), range(2))
    plt.figure(figsize = (10, 7))
    sn.set(font_scale=1.4)  # for label size
    sn.heatmap(df_cm, annot=True, annot_kws={"size": 16})  # font size
    plt.show()


def make_models(w2v=False, own=False) -> dict:
    w2v_dict = {}
    if w2v:
        if own:
            pass
            # w2v_dict = create_word_embeddings(x['supercomment'])
        else:
            w2v_dict = parse_word_vectors(util.WORDVEC_DATA)

    classifiers = [
        ("logistic regression", LogisticRegression()),
        ("GaussianNB", GaussianNB()),
        ("extra trees", ExtraTreesClassifier(n_estimators=150)),
        ("random forest", RandomForestClassifier(n_estimators=200)),
        ("svm", svm.SVC())
    ]

    return {
        label + ' with w2v' * w2v : Pipeline(
            [('embedding vectorizer', EmbeddingVectorizer(w2v_dict))] * w2v + [(label, clf)]
        )
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
            # print(label,'...')
            df = transform(df)
    return df

def cross_val() -> dict:
    df = maxiv_data.get_split_set()
    df = apply_transforms(df,['tokenizing','binarizing','tfidf'])
    print(df)
    x, y = get_xy(df)

    # models_with_word_embedding = make_models(w2v=True, own=False)
    models_without_word_embedding = make_models(w2v=False, own=False)

    # cv_precisions_with = {
    #     label: cross_val_score(model, x, y, scoring='accuracy')
    #     for label, model in models_with_word_embedding.items()
    # }

    cv_precisions_without = {
        label: cross_val_score(model, x, y, scoring='f1')
        for label, model in models_without_word_embedding.items()
    }

    return cv_precisions_without


def get_coeffs():
    df = maxiv_data.get_split_set()
    df = apply_transforms(df,['tokenizing', 'autocorrect', 'binarizing', 'tfidf'])
    x, y = get_xy(df)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33)
    lr = LogisticRegression()
    lr.fit(x_train, y_train)
    predicted = lr.predict(x_test)
    print('accuracy: ', accuracy_score(y_test, predicted))
    print('f1: ', f1_score(y_test, predicted))
    print('confusion matrix: \n', confusion_matrix(y_test, predicted))
    tups = zip(lr.coef_[0], list(x))
    return sorted(list(tups))

def plot_cross_val():
    for label, transforms in [# ('tfidf', ['tfidf']),
                              # ('embedding',['embedding']),
                              ('tfidf_embedding', ['tfidf', 'embedding'])
                              ]:
        df = maxiv_data.get_split_set()
        df = apply_transforms(df,['tokenizing', 'binarizing'] + transforms)
        x, y = get_xy(df)
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.33)
        # print(y_test)
        lr = LogisticRegression(class_weight='balanced')
        # lr.fit(x_train,y_train)
        predicted = cross_val_predict(lr,x,y)
        print(predicted)
        confusion_matrix = ConfusionMatrix(y, predicted)
        # print(confusion_matrix)
        print(f1_score(y,predicted))
        confusion_matrix.plot()
        plt.show()

def cross_dataset_eval():
    train = amazon_data.get_set()
    test = maxiv_data.get_set()
    print('loaded datasets')
    train = apply_transforms(train)
    test = apply_transforms(test)
    print('applied transforms')
    train_x, train_y = get_xy(train)
    test_x, test_y = get_xy(test)
    models = make_models(w2v=True, own=False)
    scores = {}
    for label, model in models.items():
        print('training',label,'...')
        model.fit(train_x,train_y)
        pred_y = model.predict(test_x)
        scores[label] = accuracy_score(test_y, pred_y)
    return scores


