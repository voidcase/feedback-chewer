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
    print(confusion_matrix(y_test,y_predict))
    print("Logistic regression. \n target:",scoretype,'\ncross_val_scores: ',scores)

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
    return model.score(x_test, y_test) # coefficient of determination R^2

if __name__ == '__main__':
    logisticRegression(util.TARGET)
    #print('score: ', eval_model(util.TARGET))
    #print_cross_val_scores(util.TARGET)
