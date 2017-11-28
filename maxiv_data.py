import pandas as pd
import util

def _all_scores(row:pd.Series) -> list:
    return [row[h] for h in util.SCORE_TYPES]

def unify_avg(df:pd.DataFrame) -> pd.DataFrame:
    df['score'] = df.apply(lambda row: sum(_all_scores(row))/len(_all_scores(row)))
    return df


def unify_lowest(df:pd.DataFrame) -> pd.DataFrame:
    df['score'] = df.apply(lambda row: min([row[h] for h in util.SCORE_TYPES]), axis=1)
    df = df.drop(util.SCORE_TYPES, axis=1)
    return df

def unify_text(df:pd.DataFrame) -> pd.DataFrame:
    df['text'] = ""
    for header in util.TEXT_HEADERS:
        df['text'] += df[header]
    df = df.drop(util.TEXT_HEADERS, axis=1)
    return df


def read_file(filename=util.FEEDBACK_DATA, drop_empty=True):
    df = pd.read_csv(util.FEEDBACK_DATA)[util.TEXT_HEADERS + util.SCORE_TYPES]
    if drop_empty:
        df = df.dropna(subset=util.TEXT_HEADERS, how='all')
    df = df.fillna('')
    df = df.drop(df[df['Overall'] == 0].index)
    return df


def get_set() -> pd.DataFrame:
    """
    :return: dataframe will have headers 'text':str and 'score':int between 1 and 5
    """
    df = read_file()
    df = unify_text(df)
    df = unify_lowest(df)
    return df


if __name__ == '__main__':
    print(get_set())