import numpy as np

class EmbeddingVectorizer():
    def __init__(self, w2v_dict):
        self.w2v_dict = w2v_dict

    def fit(self, x, y):
        return self

    def transform(self, x):
            vectors = [np.mean([self.w2v_dict[w] for w in comment if w in self.w2v_dict]
                               or [np.zeros(256)])
                       for comment in x]
            return np.array(vectors)







