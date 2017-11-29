import pandas as pd
import wordset
import autocorrect

def _split_text(comment:str) -> list:
    return [c.lower() for c in wordset.tokenize(comment)]

def token_transform(df:pd.DataFrame) -> pd.DataFrame:
    """
    :param df: req text
    :return: +tokens -text
    """
    ret = df.copy() #type: pd.DataFrame
    ret['tokens'] = df.apply(lambda row: _split_text(row['text']),axis=1)
    ret = ret.drop('text',axis=1)
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