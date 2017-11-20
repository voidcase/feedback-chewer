import util
from sklearn.pipeline import Pipeline
from sklearn import svm
from embedding_vectorizer import EmbeddingVectorizer
from data_extractor import get_x_and_y, parse_word_vectors

w2v_dict = parse_word_vectors(util.WORDVEC_DATA)
x, y = get_x_and_y()

svm_w2v = Pipeline(["tokenizer",
    "embedding vectorizer", EmbeddingVectorizer(w2v_dict),
                    "svm", svm.SVC()])