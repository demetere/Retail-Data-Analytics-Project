from __future__ import division

# do not show warnings
import warnings


warnings.filterwarnings("ignore")


# import machine learning related libraries
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold, cross_val_score
import xgboost as xgb



def select_best_model(X_train, y_train, X_test, y_test):
    # This is to measure models
    # Create an array of models
    global best_model
    models = []
    models.append((('LR', LogisticRegression())))
    models.append(('NB', GaussianNB()))
    models.append(('RF', RandomForestClassifier()))
    models.append(('SVC', SVC()))
    models.append(("Dtree", DecisionTreeClassifier()))
    models.append(("XGB", xgb.XGBClassifier()))
    models.append(("KNN", KNeighborsClassifier()))

    best_accuracy = 0
    # Measure the accuracy
    for name, model in models:
        kfold = KFold(n_splits=2, random_state=22)
        result = cross_val_score(model, X_train, y_train, cv=kfold, scoring='accuracy')
        if(result[1]>best_accuracy):
            best_model = model
        print(name, result)

    best_model.fit(X_train,y_train)

    print('Accuracy of Model on training set: {:.2f}'
          .format(best_model.score(X_train, y_train)))
    print('Accuracy of Model on test set: {:.2f}'
          .format(best_model.score(X_test[X_train.columns], y_test)))

    return best_model
