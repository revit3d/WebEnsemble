import uuid
from enum import Enum

from pydantic import BaseModel, HttpUrl


class ModelName(str, Enum):
    random_forest = 'random_forest'
    gradient_boosting = 'gradient_boosting'


class Splitter(str, Enum):
    best = 'best'
    random = 'random'


class TreeParams(BaseModel):
    splitter: Splitter = Splitter.best
    min_samples_split: int = 2
    min_samples_leaf: int = 1
    min_weight_fraction_leaf: float = 0.0
    max_features: int | None = None
    random_state: int | None = None
    max_leaf_nodes: int | None = None
    min_impurity_decrease: float = 0.0
    ccp_alpha: float = 0.0


class RFParams(BaseModel):
    n_estimators: int
    max_depth: int | None = None
    feature_subsample_size: float | None = None


class GBParams(BaseModel):
    n_estimators: int
    learning_rate: float = 0.1
    max_depth: int = 5
    feature_subsample_size: float | None = None


class MLModelBase(BaseModel):
    pass


class MLModelOut(MLModelBase):
    uuid: uuid.UUID
    train_file: HttpUrl | None = None
    val_file: HttpUrl | None = None
    train_loss: list | None = None
    val_loss: list | None = None


class RFModelIn(MLModelBase):
    ensemble_params: RFParams
    tree_params: TreeParams


class GBModelIn(MLModelBase):
    ensemble_params: GBParams
    tree_params: TreeParams


class RFModelOut(RFModelIn, MLModelOut):
    pass


class GBModelOut(GBModelIn, MLModelOut):
    pass


class PredictInfoOut(BaseModel):
    y_preds: list
