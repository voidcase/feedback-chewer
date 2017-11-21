import util
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from embedding_vectorizer import EmbeddingVectorizer
from data_extractor import data_extract_comments, parse_word_vectors, data_extract_tfidf_comments, create_word_embeddings

def cross_validate() -> dict:
    w2v_dict = parse_word_vectors(util.WORDVEC_DATA)
    x, y = data_extract_comments()
    tfidf_matrix = data_extract_tfidf_comments()
    #w2v_own_dict = create_word_embeddings(x['supercomment'])
    classifiers = [
        ("logistic regression", LogisticRegression()),
        ("GaussianNB", GaussianNB()),
        ("extra trees", ExtraTreesClassifier(n_estimators=150)),
        ("random forest", RandomForestClassifier(n_estimators=200)),
        ("svm", svm.SVC())
    ]

    models_with_word_embedding = {
        label: Pipeline([
            ('embedding vectorizer', EmbeddingVectorizer(w2v_dict)),
            (label, clf)
        ])
        for label, clf in classifiers
    }
    models_without_word_embedding = {
        label + " without wordembedding": Pipeline([
            (label, clf)
        ])
        for label, clf in classifiers
    }

    cv_precisions_with = {
        label: cross_val_score(model, x, y, scoring='f1')
        for label, model in models_with_word_embedding.items()
    }

    cv_precisions_without = {
        label: cross_val_score(model, tfidf_matrix, y, scoring='f1')
        for label, model in models_without_word_embedding.items()
    }

    cv_precisions = {**cv_precisions_with, **cv_precisions_without}
    return cv_precisions
