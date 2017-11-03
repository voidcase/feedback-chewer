import csv
from sklearn import linear_model
from sklearn.model_selection import cross_val_score

SCORE_TYPES = [
    'Overall',
    'Scientific support',
    'Technical support',
    'Beamline hardware',
    'Beamline software',
    'Machine operation',
    'DUO'
    ]

def get_column(col):
    with open('dataset.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row[col] for row in reader]

def train_on(scoretype='Overall'):
    if scoretype not in SCORE_TYPES:
        return None
    clf = linear_model.LogisticRegression()
    X = None # TODO: get features
    y = get_column(scoretype)
    return clf.fit(X, y)

def print_cross_val_scores(scoretype='Overall'):
    if scoretype not in SCORE_TYPES: return None
    clf = linear_model.LogisticRegression()
    X = None
    y = get_column(scoretype)
    scores = cross_val_score(clf, X, y)
    print(scores)

