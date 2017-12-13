import data_extractor as data
import pandas as pd
import re

def find_context(comment:str, keyword:str) -> list:
    df = data.dependency_parse(comment)
    keywords = re.split(' ', keyword)
    keyword_rows = []
    for keyword in keywords:
        keyword_df = df[df['form'] == keyword]
        keyword_rows.append(keyword_df)
    keyword_frame = pd.concat(keyword_rows) #type:pd.DataFrame
    keyword_ids = keyword_frame['#id'].values
    keyword_heads = keyword_frame['head'].values
    keyword_tups = zip(keyword_ids, keyword_heads)
    dataframe_rows = []
    for id, head in keyword_tups:
        rows = df[( (df['head'] == id) &    #childs but not all
                    (df['deprel'] != 'conj') &
                    (df['deprel'] != 'cc') &
                    (df['deprel'] != 'nmod')
                  )
                  |
                  ( df['#id'] == head )     #parents
                  |
                  ( (df['head'] == head) &  #compounds
                    (df['deprel'] == 'compound') &
                    (df['#id'] != id)
                  )
        ]
        dataframe_rows.append(rows)
    dataframe_rows.append(keyword_frame)
    dataframe = pd.concat(dataframe_rows) #type:pd.DataFrame
    start_indices = list(int(i) for i in dataframe['start'].values)
    return start_indices

if __name__ == '__main__':
    print(type(find_context("When we arrived to the lab, the beamline was on fire.", "beamline")[0]))