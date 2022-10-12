import numpy as np
import math
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from hyperopt import tpe, hp, fmin, STATUS_OK,Trials
from hyperopt.pyll.base import scope
from sklearn.model_selection import cross_val_score


def hyperparameter_tune(X_train,y_train):
    
    # Set up space dictionary with specified hyperparameters
    space = {'n_estimators': hp.uniform('n_estimators', 75,150),
            'max_depth': hp.uniform('max_depth', 1,100),'min_samples_leaf': hp.uniform('min_samples_leaf', 1,10),
            'min_samples_split': hp.uniform('min_samples_split', 2,10),'max_samples': hp.uniform('max_samples',0,1),
            'warm_start': hp.choice('warm_start',[True, False])}
    
    # Set up objective function
    def objective(params):
        params = {'n_estimators': int(params['n_estimators']),
                'max_depth': int(params['max_depth']),'min_samples_leaf': int(params['min_samples_leaf']),
                'min_samples_split': int(params['min_samples_split']),'max_samples': params['max_samples'],
                'warm_start': params['warm_start']
                }
        # scoring method can be 'accuracy','f1','ROC','MCC' etc
        clf = RandomForestClassifier(class_weight="balanced", **params) 
        best_score = cross_val_score(clf, X_train, y_train, scoring='f1', cv=7, n_jobs=-1).mean()
        loss = 1 - best_score
        return loss
    
    # Run the algorithm - test max evals
    best = fmin(fn=objective,space=space, max_evals=50, algo=tpe.suggest)

    max_depth = int(best['max_depth'])
    max_samples = best['max_samples']
    min_samples_leaf = int(best['min_samples_leaf'])
    min_samples_split = int(best['min_samples_split'])
    n_estimators = int(best['n_estimators'])
    warm_start = int(best['warm_start'])
    
    if warm_start == 0:
        warm_start = 'True'
    elif warm_start == 1:
        warm_start = 'False'
        
    tuned_clf = RandomForestClassifier(class_weight="balanced",
                                    max_depth= max_depth,
                                    max_samples= max_samples,
                                    min_samples_leaf= min_samples_leaf,
                                    min_samples_split= min_samples_split,
                                    n_estimators= n_estimators,
                                    warm_start= False)
    
    return tuned_clf