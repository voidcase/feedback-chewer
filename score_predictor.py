import util
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score, cross_validate
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from embedding_vectorizer import EmbeddingVectorizer
from data_extractor import data_extract_comments, parse_word_vectors, data_extract_tfidf_comments, create_word_embeddings
from sklearn.metrics import confusion_matrix, make_scorer
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
import maxiv_data
import amazon_data
import transforms as tf

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

def apply_transforms(df:pd.DataFrame) -> pd.DataFrame:
    for transform in [
        tf.token_transform,
        tf.binarize_transform,
    ]:
        df = transform(df)
    return df

def cross_val() -> dict:
    df = maxiv_data.get_set()
    df = apply_transforms(df)
    x = df['tokens']
    y = df['score']
    print('xtype:', type(x))
    print('ytype:', type(y))
    #tfidf_matrix = data_extract_tfidf_comments()
    models_with_word_embedding = make_models(w2v=True, own=False)
    #models_without_word_embedding = make_models(w2v=False, own=False)

    cv_precisions_with = {
        label: cross_val_score(model, x, y, scoring='accuracy')
        for label, model in models_with_word_embedding.items()
    }

    #cv_precisions_without = {
    #    label: cross_val_score(model, tfidf_matrix, y, scoring='accuracy')
    #    for label, model in models_without_word_embedding.items()
    #}

    #cv_precisions = {**cv_precisions_with, **cv_precisions_without}
    return cv_precisions_with
