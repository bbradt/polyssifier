from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC, SVC, NuSVC
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import (RandomForestClassifier, RandomForestRegressor,
                              AdaBoostClassifier, AdaBoostRegressor,
                              BaggingClassifier, BaggingRegressor,
                              GradientBoostingRegressor, GradientBoostingClassifier)

from sklearn.linear_model import (LogisticRegression,
                                  LinearRegression,
                                  BayesianRidge, Ridge,
                                  RidgeClassifier, Lasso,
                                  ElasticNet, Lars, LassoLars,
                                  OrthogonalMatchingPursuit,
                                  PassiveAggressiveRegressor,
                                  PassiveAggressiveClassifier,
                                  SGDClassifier, Perceptron,
                                  ARDRegression, HuberRegressor,
                                  RANSACRegressor, SGDRegressor,
                                  TheilSenRegressor,
                                  ElasticNetCV,  LarsCV, LassoCV,
                                  LassoLarsCV, LogisticRegressionCV,
                                  OrthogonalMatchingPursuitCV, RidgeCV,
                                  RidgeClassifierCV)
from sklearn.naive_bayes import (GaussianNB, MultinomialNB, BernoulliNB)
from sklearn.neural_network import MLPClassifier, MLPRegressor, BernoulliRBM
from sklearn.gaussian_process import (GaussianProcessRegressor,
                                      GaussianProcessClassifier)
from sklearn.neighbors import (KNeighborsClassifier, RadiusNeighborsClassifier,
                               NearestCentroid, KNeighborsRegressor,
                               RadiusNeighborsRegressor)

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

import collections
import numpy as np
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.gaussian_process.kernels import RBF


class MyVoter(object):
    """
    Voter Classifier
    Receives fitted classifiers and runs majority voting
    """

    def __init__(self, estimators):
        '''
        estimators: List of fitted classifiers
        '''
        self.estimators_ = estimators

    def predict(self, X):
        predictions = np.asarray(
            [clf.predict(X) for clf in self.estimators_]).T
        maj = np.apply_along_axis(
            lambda x: np.argmax(np.bincount(x)), axis=1,
            arr=predictions.astype('int'))
        return maj


class MyRegressionAverager(object):
    """
    Regression averager
    Receives fitted regressors and averages the predictions of the regressors.
    """

    def __init__(self, estimators):
        '''
        estimators: List of fitted regressors
        '''
        self.estimators_ = estimators

    def predict(self, X):
        predictions = np.asarray(
            [reg.predict(X) for reg in self.estimators_]).T

        avg = np.average(predictions, axis=1)
        return avg


class MyRegressionMedianer(object):
    """
    Regression averager
    Receives fitted regressors and averages the predictions of the regressors.
    """

    def __init__(self, estimators):
        '''
        estimators: List of fitted regressors
        '''
        self.estimators_ = estimators

    def predict(self, X):
        predictions = np.asarray(
            [reg.predict(X) for reg in self.estimators_]).T

        avg = np.median(predictions, axis=1)
        return avg


def build_classifiers(exclude, scale, feature_selection, nCols):
    '''
    Input:
        - exclude: list of names of classifiers to exclude from the analysis
        - scale: True or False. Scale data before fitting classifier
        - feature_selection: True or False. Run feature selection before
        fitting classifier
        - nCols: Number of columns in input dataset to classifiers
    Output:
    Dictionary with classifier name as keys.
        - 'clf': Classifier object
        - 'parameters': Dictionary with parameters of 'clf' as keys
    '''
    classifiers = collections.OrderedDict()

    '''Neural Networks'''
    if 'Multilayer Perceptron' not in exclude:
        classifiers['Multilayer Perceptron'] = {
            'clf': MLPClassifier(),
            'parameters': {'hidden_layer_sizes': [(100, 50), (50, 25)],
                           'max_iter': [500]}
        }

    '''Neighbor Methods'''
    if 'Nearest Neighbors' not in exclude:
        classifiers['Nearest Neighbors'] = {
            'clf': KNeighborsClassifier(),
            'parameters': {'n_neighbors': [1, 5, 10, 20]}}

    if 'Radius Neighbors' not in exclude:
        classifiers['Radius Neighbors'] = {
            'clf': RadiusNeighborsClassifier(outlier_label=0),
            'parameters': {}}

    '''SVM'''
    if 'SVM' not in exclude:
        classifiers['SVM'] = {
            'clf': SVC(C=1, probability=True, cache_size=10000,
                       class_weight='balanced'),
            'parameters': {'kernel': ['rbf', 'poly'],
                           'C': [0.01, 0.1, 1]}}

    if 'Linear SVM' not in exclude:
        classifiers['Linear SVM'] = {
            'clf': LinearSVC(dual=False, class_weight='balanced'),
            'parameters': {'C': [0.01, 0.1, 1],
                           'penalty': ['l1', 'l2']}}

    '''Tree Methods'''
    if 'Decision Tree' not in exclude:
        classifiers['Decision Tree'] = {
            'clf': DecisionTreeClassifier(max_depth=None,
                                          max_features='auto'),
            'parameters': {}}

    if 'Random Forest' not in exclude:
        classifiers['Random Forest'] = {
            'clf': RandomForestClassifier(max_depth=None,
                                          n_estimators=10,
                                          max_features='auto'),
            'parameters': {'n_estimators': list(range(5, 20))}}

    '''Ensemble Methods'''
    if 'Ada Boost' not in exclude:
        classifiers['Ada Boost'] = {
            'clf': AdaBoostClassifier(),
            'parameters': {}}

    if 'Bagging' not in exclude:
        classifiers['Ada Boost'] = {
            'clf': BaggingClassifier(),
            'parameters': {}}

    if 'Gradient Boost' not in exclude:
        classifiers['Gradient Boost'] = {
            'clf': GradientBoostingClassifier(),
            'parameters': {}}

    ''' Linear Models '''
    if 'Logistic Regression' not in exclude:
        classifiers['Logistic Regression'] = {
            'clf': LogisticRegression(fit_intercept=True, solver='lbfgs',
                                      penalty='l2'),
            'parameters': {'C': [0.001, 0.1, 1]}}

    if 'Ridge Classification' not in exclude:
        classifiers['Ridge Classification'] = {
            'clf': RidgeClassifier(fit_intercept=True),
            'parameters': {}}

    if 'Ridge Classification CV' not in exclude:
        classifiers['Ridge Classification CV'] = {
            'clf': RidgeClassifierCV(fit_intercept=True),
            'parameters': {}}

    if 'Passive Aggressive' not in exclude:
        classifiers['Passive Aggressive Classifier'] = {
            'clf': PassiveAggressiveClassifier(),
            'parameters': {}}

    if 'Perceptron' not in exclude:
        classifiers['Perceptron'] = {
            'clf': Perceptron(),
            'parameters': {}}

    '''Naive Bayes'''
    if 'Gaussian Naive Bayes' not in exclude:
        classifiers['Gaussian Naive Bayes'] = {
            'clf': GaussianNB(),
            'parameters': {}}

    if 'Bernoulli Naive Bayes' not in exclude:
        classifiers['Bernoulli Naive Bayes'] = {
            'clf': BernoulliNB(),
            'parameters': {}}

    '''Discriminant Analysis'''
    if 'LDA' not in exclude:
        classifiers['LDA'] = {
            'clf': LinearDiscriminantAnalysis(),
            'parameters': {}}

    if 'QDA' not in exclude:
        classifiers['QDA'] = {
            'clf': QuadraticDiscriminantAnalysis(),
            'parameters': {}}

    if 'Gaussian Process' not in exclude:
        classifiers['Guassian Process'] = {
            'clf': GaussianProcessClassifier(),
            'parameters': {}}


    # classifiers['Voting'] = {}

    def name(x):
        """
        :param x: The name of the classifier
        :return: The class of the final estimator in lower case form
        """
        return x['clf']._final_estimator.__class__.__name__.lower()

    for key, val in classifiers.items():
        if not scale and not feature_selection:
            break
        steps = []
        if scale:
            steps.append(StandardScaler())
        if feature_selection:
            steps.append(SelectKBest(f_regression, k='all'))
        steps.append(classifiers[key]['clf'])
        classifiers[key]['clf'] = make_pipeline(*steps)
        # Reorganize paramenter list for grid search
        new_dict = {}
        for keyp in classifiers[key]['parameters']:
            new_dict[name(classifiers[key]) + '__' +
                     keyp] = classifiers[key]['parameters'][keyp]
        classifiers[key]['parameters'] = new_dict
        if nCols > 5 and feature_selection:
            classifiers[key]['parameters']['selectkbest__k'] = np.linspace(
                np.round(nCols / 5), nCols, 5).astype('int').tolist()

    return classifiers


def build_regressors(exclude, scale, feature_selection, nCols):
    '''
    This method builds an ordered dictionary of regressors, where the key is the name of the
    regressor and the value of each key contains a standard dictionary with two keys itself. The first key called
    'reg' points to the regression object, which is created by scikit learn. The second key called 'parameters'
    points to another regular map containing the parameters which are associated with the particular regression model.
    These parameters are used by grid search in polyssifier.py when finding the best model. If parameters are not
    defined then grid search is not performed on that particular regression model, so the model's default parameters
    are used instead to find the best model for the particular data.
    '''
    regressors = collections.OrderedDict()

    if 'Linear Regression' not in exclude:
        regressors['Linear Regression'] = {
            'reg': LinearRegression(),
            'parameters': {}  # Best to leave default parameters
        }

    if 'Bayesian Ridge' not in exclude:
        regressors['Bayesian Ridge'] = {
            'reg': BayesianRidge(),
            'parameters': {}  # Investigate if alpha and lambda parameters should be changed
        }

    if 'PassiveAggressiveRegressor' not in exclude:
        regressors['PassiveAggressiveRegressor'] = {
            'reg': PassiveAggressiveRegressor(),
            'parameters': {'C': [0.5, 1.0, 1.5]
                           }
        }

    if 'GaussianProcessRegressor' not in exclude:
        regressors['GaussianProcessRegressor'] = {
            'reg': GaussianProcessRegressor(),
            'parameters': {
                'alpha': [0.01, 0.1, 1.0, 10.0],
                'kernel': [RBF(x) for x in [0.01, 1.0, 100.0, 1000.0]],
            }
        }

    if 'Ridge' not in exclude:
        regressors['Ridge'] = {
            'reg': Ridge(),
            'parameters': {
                'alpha': [0.25, 0.50, 0.75, 1.00]
            }
        }

    if 'Lasso' not in exclude:
        regressors['Lasso'] = {
            'reg': Lasso(),
            'parameters': {
                'alpha': [0.25, 0.50, 0.75, 1.00]
            }
        }

    if 'Lars' not in exclude:
        regressors['Lars'] = {
            'reg': Lars(),
            'parameters': {}  # Best to leave the default parameters
        }

    if 'LassoLars' not in exclude:
        regressors['LassoLars'] = {
            'reg': LassoLars(),
            'parameters': {'alpha': [0.25, 0.50, 0.75, 1.00, 10.0]}
        }

    if 'OrthogonalMatchingPursuit' not in exclude:
        regressors['OrthogonalMatchingPursuit'] = {
            'reg': OrthogonalMatchingPursuit(),
            'parameters': {}  # Best to leave default parameters
        }

    if 'ElasticNet' not in exclude:
        regressors['ElasticNet'] = {
            'reg': ElasticNet(),
            'parameters': {'alpha': [0.25, 0.50, 0.75, 1.00],
                           'l1_ratio': [0.25, 0.50, 0.75, 1.00]}
        }

    if 'ARD Regression' not in exclude:
        regressors['ARD Regression'] = {
            'reg': ARDRegression(),
            'parameters': {}  # Best to leave default parameters
        }

    if 'Huber Regression' not in exclude:
        regressors['Huber Regression'] = {
            'reg': HuberRegressor(),
            'parameters': {}  # Best to leave default parameters
        }

    if 'RANSAC Regression' not in exclude:
        regressors['RANSAC Regression'] = {
            'reg': RANSACRegressor(),
            'parameters': {}  # Best to leave default parameters
        }

    if 'SGD Regression' not in exclude:
        regressors['SGD Regression'] = {
            'reg': SGDRegressor(),
            'parameters': {}  # Best to leave default parameters
        }

    if 'TheilSen Regression' not in exclude:
        regressors['TheilSen Regression'] = {
            'reg': TheilSenRegressor(),
            'parameters': {}  # Best to leave default parameters
        }

    if 'MLP Regression' not in exclude:
        regressors['MLP Regression'] = {
            'reg': MLPRegressor(),
            'parameters': {}  # Best to leave default parameters
        }

    if 'KNN Regression' not in exclude:
        regressors['KNN Regression'] = {
            'reg': KNeighborsRegressor(),
            'parameters': {}  # Best to leave default parameters
        }

    if 'Random Forest' not in exclude:
        regressors['Random Forest'] = {
            'reg': RandomForestRegressor(),
            'parameters': {}
        }

    if 'Decision Tree' not in exclude:
        regressors['Decision Tree'] = {
            'reg': DecisionTreeRegressor(),
            'parameters': {}
        }
    
    if 'Ada Boost' not in exclude:
        regressors['Ada Boost'] = {
            'clf': AdaBoostRegressor(),
            'parameters': {}}

    if 'Bagging' not in exclude:
        regressors['Ada Boost'] = {
            'clf': BaggingRegressor(),
            'parameters': {}}

    if 'Gradient Boost' not in exclude:
        regressors['Gradient Boost'] = {
            'clf': GradientBoostingRegressor(),
            'parameters': {}}

    

    def name(x):
        """
        :param x: The name of the regressor
        :return: The class of the final regression estimator in lower case form
        """
        return x['reg']._final_estimator.__class__.__name__.lower()

    for key, val in regressors.items():
        if not scale and not feature_selection:
            break
        steps = []
        if scale:
            steps.append(StandardScaler())
        if feature_selection:
            steps.append(SelectKBest(f_regression, k='all'))
        steps.append(regressors[key]['reg'])
        regressors[key]['reg'] = make_pipeline(*steps)
        # Reorganize paramenter list for grid search
        new_dict = {}
        for keyp in regressors[key]['parameters']:
            new_dict[name(regressors[key]) + '__' +
                     keyp] = regressors[key]['parameters'][keyp]
        regressors[key]['parameters'] = new_dict
        if nCols > 5 and feature_selection:
            regressors[key]['parameters']['selectkbest__k'] = np.linspace(
                np.round(nCols / 5), nCols, 5).astype('int').tolist()

    return regressors
