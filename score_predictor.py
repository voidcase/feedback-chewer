import util
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from embedding_vectorizer import EmbeddingVectorizer
from data_extractor import data_extract_comments, parse_word_vectors, create_word_embeddings

w2v_dict = parse_word_vectors(util.WORDVEC_DATA)
x, y = data_extract_comments()
w2v_own_dict = create_word_embeddings(x['supercomment'])

svm_w2v = Pipeline([("embedding vectorizer", EmbeddingVectorizer(w2v_dict)),
                    ("svm", svm.SVC(kernel='linear'))])

logr_w2v = Pipeline([("embedding vectorizer", EmbeddingVectorizer(w2v_dict)),
                    ("logistic regression", LogisticRegression())])

nb_w2v = Pipeline([("embedding vectorizer", EmbeddingVectorizer(w2v_dict)),
                    ("logistic regression", GaussianNB())])

etrees_w2v = Pipeline([("embedding vectorizer", EmbeddingVectorizer(w2v_dict)),
                    ("extra trees", ExtraTreesClassifier(n_estimators=150))])

randomforest_w2v = Pipeline([("embedding vectorizer", EmbeddingVectorizer(w2v_dict)),
                    ("extra trees", RandomForestClassifier(n_estimators=200))])

# cv_score_nb = cross_val_score(nb_w2v,x,y)
# cv_score_logr = cross_val_score(logr_w2v, x, y)
# cv_score_etrees = cross_val_score(etrees_w2v,x,y)
# cv_score_randomforest = cross_val_score(randomforest_w2v,x,y,scoring='precision')
# cv_score_svm_w2v = cross_val_score(svm_w2v,x,y)
# print(cv_score_svm_w2v)



