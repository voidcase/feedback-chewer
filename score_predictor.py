import csv
from sklearn import linear_model
from sklearn.model_selection import cross_val_score, train_test_split
import data_extractor
import util
import matplotlib.pyplot as plt
from pprint import pprint


def get_int_column(col):
    with open('dataset.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        return [int(row[col]) for row in reader]


def print_cross_val_scores(scoretype='Overall'):
    if scoretype not in util.SCORE_TYPES:
        return None
    clf = linear_model.LinearRegression()
    x = data_extractor.data_extract()
    y = get_int_column(scoretype)
    scores = cross_val_score(clf, x, y)
    print(scores)


def eval_model():
    x_all = data_extractor.data_extract()
    y_all = get_int_column('Overall')
    x_train, x_test, y_train, y_test = train_test_split(x_all, y_all, test_size=0.1)
    model = linear_model.LinearRegression().fit(x_train, y_train)
    coefficients = model.coef_
    zipped = zip(coefficients, list(x_train))
    pprint(sorted(list(zipped))[-10:])

    # plt.plot(y_test,model.predict(x_test), 'bo')
    return model.score(x_test, y_test)


if __name__ == '__main__':
    print(eval_model())
