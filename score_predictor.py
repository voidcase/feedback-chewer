import csv
import pandas_ml
from sklearn import linear_model
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
import data_extractor
import util
import matplotlib.pyplot as plt
from pprint import pprint

def logisticRegression(config=util.DEFAULT_CONFIG):
    if config['target'] not in util.SCORE_TYPES:
        return None
    clf = linear_model.LogisticRegression()
    x, y = data_extractor.get_x_and_y(config)
    scores = cross_val_score(clf, x, y , cv=5)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    model = clf.fit(x_train,y_train)
    y_predict = model.predict(x_test)
    # C_(i,j) is number of observations known to be in group i but predicted to be in j
    confusionmatrix = pandas_ml.ConfusionMatrix(y_test, y_predict)
    confusionmatrix.plot(title='logistic regression')
    confusionmatrix.print_stats()
    plt.show()
    print("Logistic regression. \ntarget:",config['target'],'\ncross_val_scores: ',scores)
    coefficients = model.coef_
    for category in coefficients:
        zipped = zip(category, list(x_train))
        pprint(sorted(list(zipped)))

#almost same method as logisticregression, apart from the classifier
def svm(config=util.DEFAULT_CONFIG):
    if config['target'] not in util.SCORE_TYPES:
        return None
    clf = SVC(kernel='linear')
    x, y = data_extractor.get_x_and_y(config)
    scores = cross_val_score(clf, x, y , cv=5)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    model = clf.fit(x_train,y_train)
    y_predict = model.predict(x_test)
    # C_(i,j) is number of observations known to be in group i but predicted to be in j
    confusionmatrix = pandas_ml.ConfusionMatrix(y_test, y_predict)
    confusionmatrix.plot()
    confusionmatrix.print_stats()
    plt.show()
    print("SVM \ntarget:",config['target'],'\ncross_val_scores: ',scores)

def cross_val_linr(config=util.DEFAULT_CONFIG):
    if config['target'] not in util.SCORE_TYPES:
        return None
    clf = linear_model.LinearRegression()
    x, y = data_extractor.get_x_and_y(config)
    scores = cross_val_score(clf, x, y , cv=5)
    print("target: ", config['target'], '\ncross_val_scores: ', scores)

def coefficients_linr(config=util.DEFAULT_CONFIG):
    x, y = data_extractor.get_x_and_y(config)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    model = linear_model.LinearRegression().fit(x_train, y_train)
    coefficients = model.coef_
    zipped = zip(coefficients, list(x_train))
    print("coefficients: " )
    pprint(sorted(list(zipped)))
    print(model.score(x_test, y_test)) # coefficient of determination R^2

def confusion_matrix_linr(config=util.DEFAULT_CONFIG):
    x, y = data_extractor.get_x_and_y(config)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    model = linear_model.LinearRegression().fit(x_train, y_train)
    y_pred = model.predict(x_test)
    y_pred_round = [round(x, 0) for x in y_pred]
    confusionmatrix = pandas_ml.ConfusionMatrix(y_test, y_pred_round)
    confusionmatrix.plot()
    plt.show()

if __name__ == '__main__':
    config = util.DEFAULT_CONFIG
    #logisticRegression()
    svm()
    #coefficients_linr()
    #cross_val_linr()
    #confusion_matrix_linr()