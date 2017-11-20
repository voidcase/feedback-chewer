import numpy as np
import pandas as pd
class EmbeddingVectorizer():
    def __init__(self, w2v_dict):
        self.w2v_dict = w2v_dict

    def fit(self, x, y):
        return self

    def transform(self, x:pd.DataFrame):
            vectors = [np.mean([self.w2v_dict[w] for w in comment if w in self.w2v_dict]
                               or [np.zeros(256)], axis=0) for comment in x['supercomment']]
            print()
            return vectors







