import data_extractor as data
import re
import util
from comment import Comment


def find_posi_nega_tokens(comment: Comment) -> (list, list):
    positives = data.get_txt_lineset(util.POSITIVE_DATA)
    negatives = data.get_txt_lineset(util.NEGATIVE_DATA)
    tokens = [x.lower() for x in comment.lemmas]
    nega_indices = [i for i, w in enumerate(tokens) if w in negatives]
    posi_indices = [i for i, w in enumerate(tokens) if w in positives]
    return (posi_indices, nega_indices)


def find_nps(comment: Comment, positokens, negatokens) -> (set, set):
    properties = comment.properties
    objects = [i for i, w in enumerate(properties) if w in ['nsubj', 'dobj']]
    subjects = [i for i, w in enumerate(properties) if w in ['amod']]
    posi, nega = find_posi_nega_tokens(comment)
    relevant_connections = [comment.connections[i] for i in objects] + \
                           [reversed(comment.connections[j]) for j in subjects]
    positive_nouns , negative_nouns = set(), set()
    for j, i in relevant_connections:
        for w in posi:
            if w == i and comment.pos[j] in ['NN','NNS']:
                if is_negated(comment, i):
                    negative_nouns = negative_nouns.union(find_compound(comment, j))
                else:
                    positive_nouns = positive_nouns.union(find_compound(comment, j))
        for w in nega:
            if w == i and comment.pos[j] in ['NN','NNS']:
                if is_negated(comment, i):
                    positive_nouns = positive_nouns.union(find_compound(comment, j))
                else:
                    negative_nouns = negative_nouns.union(find_compound(comment, j))
    return positive_nouns, negative_nouns

def find_compound(comment: Comment, index) -> set:
    compounds = [i for i, w in enumerate(comment.properties) if w == 'compound']
    relevant_connections = [comment.connections[i] for i in compounds]
    compound = {index}
    for i, j in relevant_connections:
        if i == index:
            compound.add(j)
        if j == index:
            compound.add(i)
    return compound


def is_negated(comment: Comment, index):
    negations = [i for i, w in enumerate(comment.properties) if w == 'neg']
    relevant_connections = [comment.connections[i] for i in negations]
    for i, j in relevant_connections:
        if j == index:
            return True
    return False

def create_dict(comment: Comment):
    pos_tokens, neg_tokens = find_posi_nega_tokens(comment)
    pos_nouns, neg_nouns = find_nps(comment, pos_tokens, neg_tokens)
    dict = {}
    for i in range(comment.size): dict[i] = 0
    for i in pos_nouns:
        dict[i] = 1
    for i in neg_nouns: dict[i] = -1
    return dict


# cmts = re.split("[\-!?:.]+", cmt)

dataset = data.get_all_data()
comments = dataset['Experiment comments']
c = Comment('we did not like the lunch')
print(create_dict(c))
print(c.connections)
print(c.properties)



# sentiment_annotate(comments)
