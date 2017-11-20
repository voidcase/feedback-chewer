import util
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn import svm
from embedding_vectorizer import EmbeddingVectorizer
from data_extractor import data_extract_comments, parse_word_vectors

w2v_dict = parse_word_vectors(util.WORDVEC_DATA)
x, y = data_extract_comments()


svm_w2v = Pipeline([("embedding vectorizer", EmbeddingVectorizer(w2v_dict)),
                    ("svm", svm.SVC())])


cv_score = cross_val_score(svm_w2v, x, y)
print(cv_score)
