import pandas as pd
import wordset

def _split_text(comment:str) -> list:
    return [c.lower() for c in wordset.tokenize(comment)]

def token_transform(df:pd.DataFrame):
    """
    req headers: text
    header diff: +tokens -text
    :return:
    """
    ret = df.copy()
    ret['tokens'] = df.apply(lambda row: _split_text(row['text']),axis=1)
    ret = ret.drop('text',axis=1)
    return ret

def binarize_transform(df:pd.DataFrame) -> pd.DataFrame:
    """
    :param df: req score
    :return: ~score
    """
    ret = df.copy()
    ret['score'] = df.apply(lambda row: 1 if row['score'] > 3 else 0, axis=1)
    return ret