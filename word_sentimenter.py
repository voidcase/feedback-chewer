import data_extractor as data
import re
import util
from comment import Comment
from pprint import pprint


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
    positive_nouns, negative_nouns = set(), set()
    for j, i in relevant_connections:
        for w in posi:
            if w == i and comment.pos[j] in ['NN', 'NNS']:
                if has_connection(comment, i, 'neg'):
                    negative_nouns = negative_nouns.union(find_compound_conj(comment, j))
                else:
                    positive_nouns = positive_nouns.union(find_compound_conj(comment, j))
        for w in nega:
            if w == i and comment.pos[j] in ['NN', 'NNS']:
                if has_connection(comment, i, 'neg'):
                    positive_nouns = positive_nouns.union(find_compound_conj(comment, j))
                else:
                    negative_nouns = negative_nouns.union(find_compound_conj(comment, j))
    return positive_nouns, negative_nouns


def find_compound_conj(comment: Comment, index) -> set:
    compounds = [i for i, w in enumerate(comment.properties) if w in ['compound', 'conj', 'ccomp']]
    relevant_connections = [comment.connections[i] for i in compounds]
    compound = {index}
    for i, j in relevant_connections:
        if i == index and not has_connection(comment, j, 'amod'):  # e.g. for case 'excellent beamline but bad support'
            compound.add(j)
        if j == index and not has_connection(comment, i, 'amod'):
            compound.add(i)
    return compound


def has_connection(comment: Comment, index, conn_label) -> bool:
    connections = [i for i, w in enumerate(comment.properties) if w == conn_label]
    relevant_connections = [comment.connections[i] for i in connections]
    for i, j in relevant_connections:
        if j == index or i == index:
            return True
    return False


def create_dict(comment: Comment):
    pos_tokens, neg_tokens = find_posi_nega_tokens(comment)
    pos_nouns, neg_nouns = find_nps(comment, pos_tokens, neg_tokens)
    dict = {}
    # 0 is neutral, 1 is positive and -1 is negative
    #for i in range(comment.size): dict[comment.lemmas[i]] = 0
    for i in pos_nouns:
        dict[comment.lemmas[i]] = 1
    for i in neg_nouns: dict[comment.lemmas[i]] = -1
    return dict

if __name__ == '__main__':
    # comments = data.get_all_data()['Experiment comments']
    # positive_nps = set()
    # negative_nps = set()
    # for cmt in comments:
    #     cmts = re.split('[\.!:-]', cmt)
    #     for line in cmts:
    #         comment = Comment(line)
    #         posi, nega = find_posi_nega_tokens(comment)
    #         posi_np, nega_np = find_nps(comment, posi, nega)
    #         posi_np = [comment.lemmas[i] for i in posi_np]
    #         nega_np = [comment.lemmas[i] for i in nega_np]
    #         print(cmt)
    #         positive_nps = positive_nps.union(posi_np)
    #         negative_nps = negative_nps.union(nega_np)
    #     print(positive_nps)

    c = Comment('the beam was instable')
    posi, nega = find_posi_nega_tokens(c)
    posnps, negnps = find_nps(c,posi,nega)
    print(posi, nega)
    print(posnps, negnps)
    dict = create_dict(c)
    pprint(dict)