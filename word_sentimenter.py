import data_extractor as data
import util
from comment import Comment

def find_posi_nega_tokens(comment: Comment) -> (list, list):
    positives = data.get_txt_lineset(util.POSITIVE_DATA)
    negatives = data.get_txt_lineset(util.NEGATIVE_DATA)
    tokens = [x.lower() for x in comment.lemmas]
    nega_indices = [i for i, w in enumerate(tokens) if w in negatives]
    posi_indices = [i for i, w in enumerate(tokens) if w in positives]
    return(posi_indices, nega_indices)

def find_adj(comment: Comment):
    properties = comment.properties
    print(comment.properties)
    print(comment.connections)
    return [i for i, w in enumerate(properties) if w == 'nsubj']
