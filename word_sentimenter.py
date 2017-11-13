import data_extractor as data
import util

def sentiment_annotate(comment: str) -> (list, list):
    positives = data.get_txt_lineset(util.POSITIVE_DATA)
    negatives = data.get_txt_lineset(util.NEGATIVE_DATA)
    parsed = data.dependency_parse(comment)
    tokens = next((n for n in parsed['nodes'] if n['layer'].split('.')[-1] == 'Token'))['nodes'][0]['properties']
    negatokens_indices = [i for i, w in enumerate(tokens) if w['lemma'] in negatives]
    positokens_indices = [i for i, w in enumerate(tokens) if w['lemma'] in positives]
    print(tokens)
    print('negatokens:',[tokens[i] for i in negatokens_indices])
    print('positokens:',[tokens[i] for i in positokens_indices])