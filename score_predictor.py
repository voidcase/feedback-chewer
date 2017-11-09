import csv
from sklearn import linear_model
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import confusion_matrix
import data_extractor
import util
import matplotlib.pyplot as plt
from pprint import pprint

def logisticRegression(scoretype='Overall'):
    if scoretype not in util.SCORE_TYPES:
        return None
    clf = linear_model.LogisticRegression()
    x, y = data_extractor.getXandY(scoretype)
    scores = cross_val_score(clf, x, y , cv=5)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)
    model = clf.fit(x_train,y_train)
    y_predict = model.predict(x_test)
    # C_(i,j) is number of observations known to be in group i but predicted to be in j
    print(confusion_matrix(y_test,y_predict,labels = [0,1,2,3,4,5]))
    print("Logistic regression. \ntarget:",scoretype,'\ncross_val_scores: ',scores)
    coefficients = model.coef_
    for category in coefficients:
        zipped = zip(category, list(x_train))
        pprint(sorted(list(zipped)))

def print_cross_val_scores(config=util.DEFAULT_CONFIG):
    if config['target'] not in util.SCORE_TYPES:
        return None
    clf = linear_model.LinearRegression()
    x, y = data_extractor.get_x_and_y(config)
    scores = cross_val_score(clf, x, y , cv=5)
    print("target: ", config['target'], '\ncross_val_scores: ', scores)

def eval_model(config=util.DEFAULT_CONFIG):
    x, y = data_extractor.get_x_and_y(config)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)
    model = linear_model.LinearRegression().fit(x_train, y_train)
    #plt.plot(y_test,model.predict(x_test), 'bo')
    #plt.show()
    coefficients = model.coef_
    zipped = zip(coefficients, list(x_train))
    print("coefficients: " )
    pprint(sorted(list(zipped)))
    return model.score(x_test, y_test) # coefficient of determination R^2

if __name__ == '__main__':
    config = util.DEFAULT_CONFIG

    print('score: ', eval_model())
    print_cross_val_scores()
