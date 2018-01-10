import pandas as pd
import numpy as np
import data_extractor
import util
import autocorrect
import pickle
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer

def _split_text(comment:str) -> list:
    return [c.lower() for c in re.findall('\w+', comment)]

def token_transform(df:pd.DataFrame) -> pd.DataFrame:
    """
    :param df: req text
    :return: +tokens
    """
    ret = df.copy() #type: pd.DataFrame
    ret['tokens'] = df.apply(lambda row: _split_text(row['text']),axis=1)
    ret['drop'] = [len(item) != 0 for item in ret['tokens']]
    ret = ret[ret['drop']].drop(['drop'], axis=1)
    return ret

def tfidf_transform(df:pd.DataFrame) -> pd.DataFrame:
    ret = df.reset_index(drop=True).copy() #type:pd.DataFrame
    values = df['text'].values
    vectorizer = TfidfVectorizer(stop_words='english', min_df=util.MIN_DF, ngram_range=(1,3))
    tfidf_matrix = vectorizer.fit_transform(values).toarray()
    featurenames = np.asarray(vectorizer.get_feature_names())
    tfidf_frame = pd.DataFrame(tfidf_matrix,columns=featurenames)
    ret = pd.concat([ret, tfidf_frame], axis=1) #type:pd.DataFrame
    ret = ret.drop('text', axis=1)
    return ret

def embedding_transform(df:pd.DataFrame) -> pd.DataFrame:
    ret = df.reset_index(drop=True).copy() #type: pd.DataFrame
    w2v_dict = data_extractor.parse_word_vectors(util.WORDVEC_DATA)
    vectors = np.array([np.mean([w2v_dict[w] for w in comment if w in w2v_dict]
                                or [np.zeros(util.NUMBER_DIMENSIONS)], axis=0) for comment in ret['tokens'].values])
    vector_frame = pd.DataFrame(vectors)
    ret = pd.concat([ret, vector_frame], axis=1)  # type:pd.DataFrame
    ret = ret.drop('tokens', axis=1)
    return ret


def binarize_transform(df:pd.DataFrame) -> pd.DataFrame:
    """
    :param df: req score
    :return: ~score
    """
    ret = df.copy() #type: pd.DataFrame
    ret['score'] = df.apply(lambda row: 1 if row['score'] >= 3.5 else 0, axis=1)
    return ret

def _spell_and_cache(word:str, cache:dict) -> str:
    if word not in cache:
        cache[word] = autocorrect.spell(word)
    return cache[word]

def auto_correct_transform(df:pd.DataFrame) -> pd.DataFrame:
    """
    :param df: req tokens
    :return: ~tokens
    """
    cache = {}
    if os.path.exists(util.AUTOCORRECT_PICKLE_FILE):
        cache = pickle.load(open(util.AUTOCORRECT_PICKLE_FILE, 'rb'))
    ret = df.copy() #type: pd.DataFrame
    ret['tokens'] = ret.apply(lambda row: [_spell_and_cache(t,cache) for t in row['tokens']],axis=1)
    pickle.dump(cache,open(util.AUTOCORRECT_PICKLE_FILE, 'wb'))
    return ret


def sentence_split_transform(df:pd.DataFrame) -> pd.DataFrame:
    """
    :param df: req text
    :return: splits rows by sentences in text
    """
    ret = pd.DataFrame(columns=list(df))
    for index, row in df.iterrows():
        sentences = re.split(r'[.?!]\s+', row['text'])
        for s in sentences:
            new_row = row.copy()
            new_row['text'] = s
            ret = pd.concat([ret, pd.DataFrame([new_row])],ignore_index=True)
    return ret


