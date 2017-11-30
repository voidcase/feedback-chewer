import pandas as pd
import numpy as np
import data_extractor
import wordset
import util
import autocorrect
from sklearn.feature_extraction.text import TfidfVectorizer

def _split_text(comment:str) -> list:
    return [c.lower() for c in wordset.tokenize(comment)]

def token_transform(df:pd.DataFrame) -> pd.DataFrame:
    """
    :param df: req text
    :return: +tokens
    """
    ret = df.copy() #type: pd.DataFrame
    ret['tokens'] = df.apply(lambda row: _split_text(row['text']),axis=1)
    # ret = ret.drop('text',axis=1)
    return ret

def tfidf_transform(df:pd.DataFrame) -> pd.DataFrame:
    ret = df.reset_index(drop=True).copy() #type:pd.DataFrame
    values = df['text'].values
    vectorizer = TfidfVectorizer(stop_words='english', min_df=util.MIN_DF)
    tfidf_matrix = vectorizer.fit_transform(values).toarray()
    featurenames = np.asarray(['word_' + w for w in vectorizer.get_feature_names()])
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
    ret['score'] = df.apply(lambda row: 1 if row['score'] > 3 else 0, axis=1)
    return ret

def auto_correct_transform(df:pd.DataFrame) -> pd.DataFrame:
    """
    :param df: req tokens
    :return: ~tokens
    """
    ret = df.copy() #type: pd.DataFrame
    ret['tokens'] = ret.apply(lambda row: [autocorrect.spell(t) for t in row['tokens']],axis=1)
    return ret