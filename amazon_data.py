import pandas as pd
import util
import json

def get_set() -> pd.DataFrame:
    """
    :return: headers text, score
    """
    rows = []
    with open(util.AMAZON_DATA,'r') as file:
        jsons = [next(file) for i in range(100000)]
        for entry in jsons:
            d = json.loads(entry,encoding='utf-8')
            assert(type(d['overall']) == float)
            rows.append({
                'text': d['reviewText'],
                'score': int(d['overall']),
            })
    return pd.DataFrame(rows)