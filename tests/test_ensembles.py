import numpy as np
from sklearn.model_selection import train_test_split

from src.ensembles import RandomForestMSE, GradientBoostingMSE


def test_random_forest():
    n_estimators = 100
    model = RandomForestMSE(
        n_estimators=n_estimators,
        max_depth=None,
        feature_subsample_size=None,
    )

    X = np.random.randint(-10000, 10000, size=(10000, 100)) / 100
    y = np.random.randint(-10000, 10000, size=(10000,)) / 100

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, train_size=0.9)

    model.fit(X_train, y_train)
    model.fit(X_train, y_train, X_val, y_val)

    assert len(model._models) == n_estimators

    model.predict(X_val)
    y_preds = model.predict(X_test)
    assert y_preds.shape == y_test.shape


def test_boosting():
    n_estimators = 100
    model = GradientBoostingMSE(
        n_estimators=n_estimators,
        learning_rate=0.1,
        max_depth=None,
        feature_subsample_size=None,
    )

    X = np.random.randint(-10000, 10000, size=(10000, 100)) / 100
    y = np.random.randint(-10000, 10000, size=(10000,)) / 100

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, train_size=0.9)

    model.fit(X_train, y_train)
    model.fit(X_train, y_train, X_val, y_val)

    assert len(model._models) == n_estimators

    model.predict(X_val)
    y_preds = model.predict(X_test)
    assert y_preds.shape == y_test.shape
