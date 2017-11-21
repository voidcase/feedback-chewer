import numpy as np
import pandas as pd
import util
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
class EmbeddingVectorizer():
    def __init__(self, w2v_dict):
        self.w2v_dict = w2v_dict
        self.weight_dict = None

    def fit(self, x, y):
        tfidf = TfidfVectorizer(stop_words=None,analyzer=lambda x: x)
        tfidf.fit(x['supercomment'])
        max_idf = max(tfidf.idf_)
        self.weight_dict = defaultdict(lambda: max_idf)
        for word, i in tfidf.vocabulary_.items():
            self.weight_dict[word] = tfidf.idf_[i]
        return self

    def transform(self, x:pd.DataFrame):
            vectors = np.array([ np.mean([self.weight_dict[w]* self.w2v_dict[w] for w in comment if w in self.w2v_dict]
                               or [np.zeros(util.NUMBER_DIMENSIONS)], axis=0) for comment in x['supercomment']])
            print('embeddingvectorizer', vectors[0])
            return vectors







