import pandas as pd
import numpy
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
    #ret = ret.drop('text',axis=1)
    return ret

def tfidf_transform(df:pd.DataFrame) -> pd.DataFrame:
    ret = df.reset_index().copy() #type:pd.DataFrame
    values = df['text'].values
    vectorizer = TfidfVectorizer(stop_words='english', min_df=util.MIN_DF)
    tfidf_matrix = vectorizer.fit_transform(values).toarray()
    #featurenames = numpy.asarray(vectorizer.get_feature_names())
    tfidf_frame = pd.DataFrame(tfidf_matrix)#  columns=featurenames)
    ret = pd.concat([ret, tfidf_frame], axis=1) #type:pd.DataFrame
    ret = ret.drop('text', axis=1)
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