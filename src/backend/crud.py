import pickle
import time
from uuid import UUID

import numpy as np
import pandas as pd

from sqlalchemy.orm import Session
from fastapi import HTTPException

import models
import schemas
import ensembles


def get_object_or_404(func):
    """Decorator for validation of a query"""
    def wrapper(*args, **kwargs):
        db_item = func(*args, **kwargs)
        if db_item is None:
            raise HTTPException(404)
        return db_item
    return wrapper


def create_model_item(db: Session,
                      model_name: str,
                      model_params: schemas.RFModelIn | schemas.GBModelIn) -> models.MLModel:
    """
    Create a new record in the \'ml_models\' table.

    Parameters:
    -------
    - db: database session
    - model_name: model architecture name
    - model_params: parameters of the defined model
    """
    db_item = models.MLModel(
        model_name=model_name,
        model_parameters=model_params.model_dump_json(),
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@get_object_or_404
def read_model_item(db: Session, uuid: UUID) -> models.MLModel:
    """Return model with the given uuid from the \'ml_models\' table"""
    return db.query(models.MLModel).where(models.MLModel.id == uuid).first()


def delete_model(db: Session, uuid: UUID) -> None:
    """Delete model with the given uuid from the \'ml_models\' table"""
    return db.delete(read_model_item(db, uuid))


def update_model(db: Session,
                 uuid: UUID,
                 model: ensembles.RandomForestMSE | ensembles.GradientBoostingMSE | None = None,
                 target_name: str | None = None,
                 train_dataset: pd.DataFrame | None = None,
                 val_dataset: pd.DataFrame | None = None,
                 train_loss: np.ndarray | None = None,
                 val_loss: np.ndarray | None = None) -> models.MLModel:
    """Update model\'s record with the given uuid."""
    db_item = read_model_item(db, uuid)

    if model is not None:
        db_item.model_serialized = pickle.dumps(model)
        db_item.is_trained = True
    if train_dataset is not None:
        db_item.train_dataset_file_path = f'storage/train/{time.perf_counter_ns()}.csv'
        train_dataset.to_csv(db_item.train_dataset_file_path)
    if val_dataset is not None:
        db_item.val_dataset_file_path = f'storage/val/{time.perf_counter_ns()}.csv'
        val_dataset.to_csv(db_item.val_dataset_file_path)
    if target_name is not None:
        db_item.target_name = target_name
    if train_loss is not None:
        db_item.train_loss = train_loss.tobytes()
    if val_loss is not None:
        db_item.val_loss = val_loss.tobytes()

    db.commit()
    db.refresh(db_item)
    return db_item
