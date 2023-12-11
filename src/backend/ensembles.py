from typing import Optional, Tuple
from joblib import Parallel, delayed

import numpy as np

from scipy.optimize import minimize_scalar
from sklearn.tree import DecisionTreeRegressor


class RandomForestMSE:
    def __init__(self,
                 n_estimators: int,
                 max_depth: Optional[int] = None,
                 feature_subsample_size: Optional[float] = None,
                 **trees_parameters) -> None:
        """
        Parameters
        -------
        - n_estimators: the number of trees in the forest.
        - max_depth: the maximum depth of the tree.\\
            If None then there is no limits.
        - feature_subsample_size: the size of feature set for each tree.\\
            If None then use one-third of all features.
        """
        self._n_estimators = n_estimators
        self._max_depth = max_depth
        self._feature_subsample_size = feature_subsample_size
        if self._feature_subsample_size is None:
            self._feature_subsample_size = 0.33
        self._tree_params = trees_parameters
        self._bagging_size = 1 - 1 / np.e
        self._models = None  # stores a tuple of (model, used features)

    def fit(self,
            X: np.ndarray,
            y: np.ndarray,
            X_val: Optional[np.ndarray] = None,
            y_val: Optional[np.ndarray] = None) -> None:
        """
        Parameters
        -------
        - X: array of size n_objects, n_features containing train samples
        - y: array of size n_objects containing train targets
        - X_val: array of size n_val_objects, n_features
        - y_val: array of size n_val_objects
        """
        if X_val is not None or y_val is not None:
            raise NotImplementedError()

        # initialize estimators
        models = []
        for _ in range(self._n_estimators):
            estimator = DecisionTreeRegressor(
                criterion='squared_error',
                max_depth=self._max_depth,
                **self._tree_params,
            )
            models.append(estimator)

        # fit estimators
        self._models = Parallel(n_jobs=-1)(
            delayed(self._fit_estimator)(X, y, model) for model in models
        )

        train_loss = self._calc_loss(X, y)

        val_loss = None
        if X_val is not None:
            val_loss = self._calc_loss(X_val, y_val)

        return train_loss, val_loss

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Parameters
        -------
        - X: array of size n_objects, n_features - the input samples

        Returns
        -------
        - y: array of size n_objects - predicted values for each input sample
        """
        if self._models is None:
            raise RuntimeError('The model is not fitted. run .fit() first.')

        preds = Parallel(n_jobs=-1)(
            delayed(self._run_estimator)(X, model) for model in self._models
        )
        return np.mean(preds, axis=0)

    def _fit_estimator(
            self,
            X: np.ndarray,
            y: np.ndarray,
            estimator: DecisionTreeRegressor):
        """
        Perform fitting of a single estimator with feature selection and bagging
        """
        # choose subsample of features for the current estimator
        ftr_subsample_size = int(self._feature_subsample_size * X.shape[1])
        ftrs_subsample = np.random.choice(
            np.arange(X.shape[1]),
            size=ftr_subsample_size,
            replace=False
        )

        # choose subsample of training samples (bagging)
        smpl_subsample_size = int(self._bagging_size * X.shape[0])
        smpls_subsample = np.random.choice(
            np.arange(X.shape[0]),
            size=smpl_subsample_size,
            replace=True
        )

        X_sub = X[smpls_subsample][:, ftrs_subsample]
        y_sub = y[smpls_subsample]

        estimator.fit(X_sub, y_sub)
        return estimator, ftrs_subsample

    def _run_estimator(self,
                       X: np.ndarray,
                       estimator: Tuple[DecisionTreeRegressor, np.ndarray]) -> np.ndarray:
        """
        Run single estimator from ensemble and collect its predictions.
        Parameters:
        -------
        - X: array of size n_objects, n_features - the input samples
        - estimator: tuple (model, feature indices used during fitting)
        """
        estimator, feature_idxs = estimator
        return estimator.predict(X[:, feature_idxs])

    def _calc_loss(self, X: np.ndarray, y: np.ndarray):
        """
        Calculate loss on each iteration of fitting the model.
        """
        preds = Parallel(n_jobs=-1)(
            delayed(self._run_estimator)(X, model) for model in self._models
        )
        preds = np.cumsum(preds, axis=0).T / (1 + np.arange(self._n_estimators))
        loss = np.mean(np.square(preds.T - y), axis=1)
        return loss


class GradientBoostingMSE:
    def __init__(self,
                 n_estimators: int,
                 learning_rate: float = 0.1,
                 max_depth: int = 5,
                 feature_subsample_size: Optional[float] = None,
                 **trees_parameters) -> None:
        """
        Parameters
        -------
        - n_estimators: The number of trees in the forest.
        - learning_rate: Use alpha * learning_rate instead of alpha
        - max_depth: The maximum depth of the tree.\\
            If None then there is no limits.
        - feature_subsample_size : The size of feature set for each tree.\\
            If None then use one-third of all features.
        """
        self._n_estimators = n_estimators
        self._lr = learning_rate
        self._max_depth = max_depth
        self._feature_subsample_size = feature_subsample_size
        if self._feature_subsample_size is None:
            self._feature_subsample_size = 0.33
        self._tree_params = trees_parameters
        self._models = None  # stores a tuple of (model, weight)

    def fit(self,
            X: np.ndarray,
            y: np.ndarray,
            X_val: Optional[np.ndarray] = None,
            y_val: Optional[np.ndarray] = None) -> None:
        """
        Parameters
        -------
        - X: Array of size n_objects, n_features containing train samples
        - y: Array of size n_objects containing train targets
        - X_val: Array of size n_val_objects, n_features
        - y_val: Array of size n_val_objects
        """
        if X_val is not None or y_val is not None:
            raise NotImplementedError()

        self._models = []
        preds = np.zeros_like(y)

        for _ in range(self._n_estimators):
            # compute antigradient
            residuals = y - preds

            # fit tree to the antigradient
            estimator = DecisionTreeRegressor(
                criterion='squared_error',
                max_depth=self._max_depth,
                **self._tree_params,
            )
            estimator, ftrs_subsample = self._fit_estimator(X, residuals, estimator)

            # find new approximation for predicions
            approx = estimator.predict(X[:, ftrs_subsample])

            # find next optimization step value
            alpha = minimize_scalar(
                fun=lambda x, p=preds, ap=approx, : np.mean(np.square(p + x * ap - y)),
                bounds=(0, 1e9),
            ).x

            # update predictions vector
            preds = preds + self._lr * alpha * approx

            self._models.append((estimator, self._lr * alpha, ftrs_subsample))

        train_loss = self._calc_loss(X, y)

        val_loss = None
        if X_val is not None:
            val_loss = self._calc_loss(X_val, y_val)

        return train_loss, val_loss

    def predict(self, X) -> np.ndarray:
        """
        Parameters
        -------
        - X: Array of size n_objects, n_features - the input samples

        Returns
        -------
        - y: Array of size n_objects - predicted values for each input sample
        """
        if self._models is None:
            raise RuntimeError('The model is not fitted. run .fit() first.')

        preds = Parallel(n_jobs=-1)(
            delayed(self._run_estimator)(X, model) for model in self._models
        )
        return np.sum(preds, axis=0)

    def _fit_estimator(self,
                       X: np.ndarray,
                       y: np.ndarray,
                       estimator: DecisionTreeRegressor):
        """
        Perform fitting of a single estimator with feature selection
        """
        ftr_subsample_size = int(self._feature_subsample_size * X.shape[1])
        ftrs_subsample = np.random.choice(
            np.arange(X.shape[1]),
            size=ftr_subsample_size,
            replace=False
        )

        X_sub = X[:, ftrs_subsample]

        estimator.fit(X_sub, y)
        return estimator, ftrs_subsample

    def _run_estimator(self,
                       X: np.ndarray,
                       estimator: Tuple[DecisionTreeRegressor, float]) -> np.ndarray:
        """
        Run single estimator from ensemble and collect its predictions.
        Parameters:
        -------
        - X: array of size n_objects, n_features - the input samples
        - estimator: tuple (model, model importance [alpha])
        """
        estimator, alpha, ftrs_subsample = estimator
        return alpha * estimator.predict(X[:, ftrs_subsample])

    def _calc_loss(self, X: np.ndarray, y: np.ndarray):
        preds = Parallel(n_jobs=-1)(
            delayed(self._run_estimator)(X, model) for model in self._models
        )
        preds = np.cumsum(preds, axis=0)
        loss = np.mean(np.square(preds - y), axis=1)
        return loss
