from sklearn.pipeline import Pipeline
from sklearn import svm
from embedding_vectorizer import EmbeddingVectorizer
from data_extractor import get_x_and_y

x, y = get_x_and_y()

svm_w2v = Pipeline(["embedding vectorizer", EmbeddingVectorizer(w2v_dict),
                    "svm", svm.SVC()])