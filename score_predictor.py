import csv
from sklearn import linear_model
from sklearn.model_selection import cross_val_score, train_test_split
import data_extractor, util
import matplotlib.pyplot as plt
from pprint import pprint

def get_int_column(col):
    with open('dataset.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        return [int(row[col]) for row in reader]

def print_cross_val_scores(scoretype='Overall'):
    if scoretype not in util.SCORE_TYPES: return None
    clf = linear_model.LinearRegression()
    X = data_extractor.data_extract()
    y = get_int_column(scoretype)
    scores = cross_val_score(clf, X, y)
    print(scores)

def eval():
    X_all = data_extractor.data_extract()
    y_all = get_int_column('Overall')
    X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=0.1)
    model = linear_model.LinearRegression().fit(X_train, y_train)
    coefficients = model.coef_
    zipped = zip(coefficients,list(X_train))
    pprint(sorted(list(zipped))[:10])

    #plt.plot(y_test,model.predict(X_test), 'bo')
    return model.score(X_test, y_test)



if __name__ == '__main__':
    print(eval())


