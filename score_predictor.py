import csv
from sklearn import linear_model
from sklearn.model_selection import cross_val_score, train_test_split
import data_extractor
import util
import matplotlib.pyplot as plt
from pprint import pprint


def print_cross_val_scores(scoretype='Overall'):
    if scoretype not in util.SCORE_TYPES:
        return None
    clf = linear_model.LinearRegression()
    x, y = data_extractor.getXandY(scoretype)
    scores = cross_val_score(clf, x, y , cv=5)
    print("target: ", scoretype, '\ncross_val_scores: ', scores)

def eval_model(scoretype='Overall'):
    x, y = data_extractor.getXandY(scoretype)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)
    model = linear_model.LinearRegression().fit(x_train, y_train)
    #plt.plot(y_test,model.predict(x_test), 'bo')
    #plt.show()
    coefficients = model.coef_
    zipped = zip(coefficients, list(x_train))
    print("coefficients: " )
    pprint(sorted(list(zipped)))
    return model.score(x_test, y_test) #coefficient of determination R^2

if __name__ == '__main__':
    print('score: ', eval_model('Beamline hardware'))
    print_cross_val_scores('Beamline hardware')
