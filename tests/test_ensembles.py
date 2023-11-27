import numpy as np
from sklearn.model_selection import train_test_split

from src.ensembles import RandomForestMSE, GradientBoostingMSE

np.random.seed(42)

X = np.random.randint(-10000, 10000, size=(10000, 100)) / 100
y = np.random.randint(-10000, 10000, size=(10000,)) / 100

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, train_size=0.9)


def test_random_forest_1():
    n_estimators = 10
    model = RandomForestMSE(
        n_estimators=n_estimators,
        max_depth=None,
        feature_subsample_size=None,
    )

    try:
        model.predict(X_val)
    except RuntimeError:
        pass
    else:
        raise AssertionError()


def test_random_forest_2():
    n_estimators = 10
    model = RandomForestMSE(
        n_estimators=n_estimators,
        max_depth=None,
        feature_subsample_size=None,
    )

    model.fit(X_train, y_train)
    assert len(model._models) == n_estimators


def test_random_forest_3():
    n_estimators = 10
    model = RandomForestMSE(
        n_estimators=n_estimators,
        max_depth=None,
        feature_subsample_size=None,
    )

    model.fit(X_train, y_train, X_val, y_val)
    assert len(model._models) == n_estimators


def test_random_forest_4():
    n_estimators = 30
    model = RandomForestMSE(
        n_estimators=n_estimators,
        max_depth=None,
        feature_subsample_size=None,
    )

    model.fit(X_train, y_train)

    model.predict(X_val)
    y_preds = model.predict(X_test)
    assert y_preds.shape == y_test.shape


def test_random_forest_5():
    n_estimators = 10
    feature_subsample_size = 0.789
    model = RandomForestMSE(
        n_estimators=n_estimators,
        max_depth=None,
        feature_subsample_size=feature_subsample_size,
    )

    model.fit(X_train, y_train)

    y_preds = model.predict(X_test)
    assert y_preds.shape == y_test.shape


def test_random_forest_6():
    n_estimators = 10
    model = RandomForestMSE(
        n_estimators=n_estimators,
        max_depth=5,
        feature_subsample_size=None,
    )

    model.fit(X_train, y_train)

    y_preds = model.predict(X_test)
    assert y_preds.shape == y_test.shape


def test_random_forest_7():
    trees_parameters = {
        'min_samples_split': 20,
        'min_samples_leaf': 5,
    }
    n_estimators = 10
    model = RandomForestMSE(
        n_estimators=n_estimators,
        max_depth=5,
        feature_subsample_size=None,
        **trees_parameters,
    )

    model.fit(X_train, y_train)

    y_preds = model.predict(X_test)
    assert y_preds.shape == y_test.shape


def test_gradient_boosting_1():
    n_estimators = 10
    model = GradientBoostingMSE(
        n_estimators=n_estimators,
        max_depth=None,
        feature_subsample_size=None,
    )

    try:
        model.predict(X_val)
    except RuntimeError:
        pass
    else:
        raise AssertionError()


def test_gradient_boosting_2():
    n_estimators = 10
    model = GradientBoostingMSE(
        n_estimators=n_estimators,
        max_depth=None,
        feature_subsample_size=None,
    )

    model.fit(X_train, y_train)
    assert len(model._models) == n_estimators


def test_gradient_boosting_3():
    n_estimators = 10
    model = GradientBoostingMSE(
        n_estimators=n_estimators,
        max_depth=None,
        feature_subsample_size=None,
    )

    model.fit(X_train, y_train, X_val, y_val)
    assert len(model._models) == n_estimators


def test_gradient_boosting_4():
    n_estimators = 30
    model = GradientBoostingMSE(
        n_estimators=n_estimators,
        max_depth=None,
        feature_subsample_size=None,
    )

    model.fit(X_train, y_train)

    model.predict(X_val)
    y_preds = model.predict(X_test)
    assert y_preds.shape == y_test.shape


def test_gradient_boosting_5():
    n_estimators = 10
    feature_subsample_size = 0.789
    model = GradientBoostingMSE(
        n_estimators=n_estimators,
        max_depth=None,
        feature_subsample_size=feature_subsample_size,
    )

    model.fit(X_train, y_train)

    y_preds = model.predict(X_test)
    assert y_preds.shape == y_test.shape


def test_gradient_boosting_6():
    n_estimators = 10
    model = GradientBoostingMSE(
        n_estimators=n_estimators,
        learning_rate=0.1,
        max_depth=5,
        feature_subsample_size=None,
    )

    model.fit(X_train, y_train)

    y_preds = model.predict(X_test)
    assert y_preds.shape == y_test.shape


def test_gradient_boosting_7():
    n_estimators = 10
    model = GradientBoostingMSE(
        n_estimators=n_estimators,
        learning_rate=1,
        max_depth=5,
        feature_subsample_size=None,
    )

    model.fit(X_train, y_train)

    y_preds = model.predict(X_test)
    assert y_preds.shape == y_test.shape


def test_gradient_boosting_8():
    trees_parameters = {
        'min_samples_split': 20,
        'min_samples_leaf': 5,
    }
    n_estimators = 10
    model = GradientBoostingMSE(
        n_estimators=n_estimators,
        learning_rate=1,
        max_depth=5,
        feature_subsample_size=None,
        **trees_parameters,
    )

    model.fit(X_train, y_train)

    y_preds = model.predict(X_test)
    assert y_preds.shape == y_test.shape
