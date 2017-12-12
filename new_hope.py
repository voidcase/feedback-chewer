import maxiv_data
from comment import Comment
import pandas as pd
from old_word_sentimenter import positivity, negativity, find_posi_nega_tokens
from pprint import pprint
from wordset import build_wordset
import transforms

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
    return [t for t in df['text'] if keyword.lower() in t.lower()]

def word_badness(keyword:str,df:pd.DataFrame):
    statements = statements_with(keyword, df)
    frequency = len(statements)
    return sum([negativity(Comment(n)) for n in statements]) / frequency

def surrounding_good_and_bad(keyword:str, df:pd.DataFrame):
    statements = statements_with(keyword, df)
    comments =  [Comment(statement) for statement in statements]
    print('wrapped in comments')
    return [find_posi_nega_tokens(c) for c in comments]

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
    df = maxiv_data.get_split_set()
    df = transforms.sentence_split_transform(df)
    #pprint(surrounding_good_and_bad("lunch", df))
    print(word_badness("support", df))
    #transforms.test_sentence_split_transform()
