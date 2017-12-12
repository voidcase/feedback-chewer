import data_extractor as data
import pandas as pd

df = data.dependency_parse('the beamline was perfect as always')
print(df)
def find_nps(df:pd.DataFrame, keyword:str):
    nps = df[(df['pos'] == 'NN') | (df['pos'] == 'NNS')]
    return nps['form'].values

def find_compounds(df:pd.DataFrame, keyword:str):
    keyword_rows = df[df['form'] == keyword]
    keyword_ids = keyword_rows['#id'].values
    keyword_heads = keyword_rows['head'].values
    keyword_tups = zip(keyword_ids, keyword_heads)
    dataframe_rows = []
    for id, head in keyword_tups:
        rows = df[( (df['head'] == id) &        #childs but not all
                    (df['deprel'] != 'conj') &
                    (df['deprel'] != 'cc') &
                    (df['deprel'] != 'nmod')
                    )
                  |
                 ( df['#id'] == head ) #parents
        ]
        dataframe_rows.append(rows)
    dataframe_rows.append(keyword_rows)
    dataframe = pd.concat(dataframe_rows)
    return dataframe
print(find_compounds(df, 'beamline'))