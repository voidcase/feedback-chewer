import maxiv_data
from comment import Comment
import pandas as pd
from word_sentimenter import positivity, negativity
from pprint import pprint
from wordset import build_wordset

def get_all_nouns() -> set:
    df = maxiv_data.get_set()
    nouns = set()
    for txt in df['text']:
        c = Comment(txt)
        noun_indices = [i for i, t in enumerate(c.tags) if t == 'NOUN']
        for i in noun_indices:
            nouns.add(c.lemmas[i])
    return nouns

def statements_with(keyword:str, df:pd.DataFrame) -> list:
    return [t for t in df['text'] if keyword in t]

def word_badness(keyword:str,df:pd.DataFrame):
    statements = statements_with(keyword, df)
    frequency = len(statements)
    return sum([positivity(Comment(n)) for n in statements]) / frequency


def get_noun_scores() -> dict:
    nouns = build_wordset()
    df = maxiv_data.get_set()
    return {
        n : sum([
            positivity(Comment(x)) for x in statements_with(n, df)
        ]) for n in nouns
    }

def test_nouns():
    nouns = get_all_nouns()
    assert type(nouns) == set
    assert len(nouns) > 0
    assert "beamline" in nouns
    assert "lab" in nouns
    assert "sufficent" not in nouns
    assert "worked" not in nouns

if __name__ == '__main__':
    df = maxiv_data.get_set()
    pprint(word_badness("chemistry", df))