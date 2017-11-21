import util
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from embedding_vectorizer import EmbeddingVectorizer
from data_extractor import data_extract_comments, parse_word_vectors, create_word_embeddings

def cross_validate() -> dict:
    w2v_dict = parse_word_vectors(util.WORDVEC_DATA)
    x, y = data_extract_comments()
    w2v_own_dict = create_word_embeddings(x['supercomment'])
    classifiers = [
        ("svm", svm.SVC()),
        ("logistic regression", LogisticRegression()),
        ("GaussianNB", GaussianNB()),
        ("extra trees", ExtraTreesClassifier(n_estimators=150)),
        ("random forest", RandomForestClassifier(n_estimators=200)),
    ]

    models_with_word_embedding = {
        label: Pipeline([
            ('embedding vectorizer', EmbeddingVectorizer(w2v_own_dict)),
            (label, clf)
        ])
        for label, clf in classifiers
    }

    cv_precisions = {
        label: cross_val_score(model, x, y, scoring='precision')
        for label, model in models_with_word_embedding.items()
    }
    return cv_precisions
