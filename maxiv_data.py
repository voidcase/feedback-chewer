import pandas as pd
import util

def _all_scores(row:pd.Series) -> list:
    return [row[h] for h in util.SCORE_TYPES]

def unify_avg(df:pd.DataFrame) -> pd.DataFrame:
    df['score'] = df.apply(lambda row: sum(_all_scores(row))/len(_all_scores(row)))
    return df

def unify_lowest(df:pd.DataFrame) -> pd.DataFrame:
    df['score'] = df.apply(lambda row: min([row[h] for h in util.SCORE_TYPES if h != 0]), axis=1)
    df = df.drop(util.SCORE_TYPES, axis=1)
    return df

def unify_text(df:pd.DataFrame) -> pd.DataFrame:
    df['text'] = ""
    for header in util.TEXT_HEADERS:
        df['text'] += " " + df[header]
    df = df.drop(util.TEXT_HEADERS, axis=1)
    return df


def split_scores_comments(df:pd.DataFrame) -> pd.DataFrame:
    dataframes = []
    for comments, scores in util.SCOREPAIRS:
        df[str(comments)] = ""
        df[str(scores)] = 0
        for comment in comments:
            df[str(comments)] += " " + df[comment]
        for score in scores:
            df[str(scores)] += df[score] / len(scores)
        temp_df = pd.DataFrame({'text': df[str(comments)], 'score': df[str(scores)]})
        dataframes.append(temp_df) #type:pd.DataFrame
    dataframe = pd.concat(dataframes) #type:pd.DataFrame
    return dataframe

def read_file(filename=util.FEEDBACK_DATA, drop_empty=True):
    df = pd.read_csv(filename)[util.TEXT_HEADERS + util.SCORE_TYPES]
    if drop_empty:
        df = df.dropna(subset=util.TEXT_HEADERS, how='all')
    df = df.fillna('')
    df = df.drop(df[df['Overall'] == 0].index)
    return df

def get_split_set() -> pd.DataFrame:
    df = read_file()
    df = split_scores_comments(df)
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