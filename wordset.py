import re
import pandas as pd

def build_wordset(dataset:pd.DataFrame, text_fields):
    wordset = set()
    for field in text_fields:
        for comment in dataset[field]:
            words = tokenize(comment)
            for word in words:
                wordset.add(word.lower())
    return wordset

def tokenize(string):
    return re.findall('\w+', string)