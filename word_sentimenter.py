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


def find_np_nsubj(comment: Comment, positokens, negatokens):
    properties = comment.properties
    subjects = [i for i, w in enumerate(properties) if w == 'nsubj']
    posi, nega = find_posi_nega_tokens(comment)
    relevant_connections = [comment.connections[i] for i in subjects]
    positive_nouns = set()
    negative_nouns = set()
    for j, i in relevant_connections:
        for w in posi:
            if w == i and comment.pos[j] == 'NN':
                if is_negated(comment, i):
                    negative_nouns.add(comment.lemmas[j])
                else:
                    positive_nouns.add(comment.lemmas[j])
        for w in nega:
            if w == i and comment.pos[j] == 'NN':
                if is_negated(comment, i):
                    positive_nouns.add(comment.lemmas[j])
                else:
                    negative_nouns.add(comment.lemmas[j])
    return positive_nouns, negative_nouns


def is_negated(comment: Comment, index):
    negations = [i for i, w in enumerate(comment.properties) if w == 'neg']
    relevant_connections = [comment.connections[i] for i in negations]
    for i, j in relevant_connections:
        if j == index:
            return True
    return False


def sentiment_annotate(comments):
    for cmt in comments[:100]:
        cmts = re.split("[\-!?:.]+", cmt)
        for cmt in cmts:
            comment = Comment(cmt)
            posi, nega = find_posi_nega_tokens(comment)
            posnouns, negnouns = find_np_nsubj(comment, posi, nega)
            if (len(negnouns) > 0):
                print(cmt)
                print(negnouns)


dataset = data.get_all_data()
comments = dataset['Experiment comments']
# c = Comment('kanelbullar are not good')
# print(c.properties)
# print(c.connections)
# print(c.pos)
# posi, nega = find_posi_nega_tokens(c)
# print(posi)
# print(find_np_nsubj(c, posi, nega))

sentiment_annotate(comments)
