import pickle
import time
from uuid import UUID

import numpy as np
import pandas as pd

from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException

import models, schemas, ensembles


def get_object_or_404(func):
    def wrapper(*args, **kwargs):
        db_item = func(*args, **kwargs)
        if db_item is None:
            raise HTTPException(404)
        return db_item
    return wrapper


def create_model_item(db: Session,
                      model_name: str,
                      model_params: schemas.RFModelIn | schemas.GBModelIn) -> models.MLModel:
    db_item = models.MLModel(
        model_name=model_name,
        model_parameters=model_params.model_dump_json(),
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@get_object_or_404
def read_model_item(db: Session, id: UUID) -> models.MLModel:
    return db.query(models.MLModel).where(models.MLModel.id == id).first()


def delete_model(db: Session, id: UUID) -> None:
    return db.delete(read_model_item(db, id))


def update_model(db: Session,
                 id: UUID,
                 model: ensembles.RandomForestMSE | ensembles.GradientBoostingMSE | None = None,
                 target_name: str | None = None,
                 train_dataset: pd.DataFrame | None = None,
                 val_dataset: pd.DataFrame | None = None,
                 train_loss: np.ndarray | None = None,
                 val_loss: np.ndarray | None = None) -> models.MLModel:
    db_item = read_model_item(db, id)

    if model is not None:
        db_item.model_serialized = pickle.dumps(model)
        db_item.is_trained = True
    if train_dataset is not None:
        db_item.train_dataset_file_path = 'storage/train/{}.csv'.format(time.perf_counter_ns())
        train_dataset.to_csv(db_item.train_dataset_file_path)
    if val_dataset is not None:
        db_item.val_dataset_file_path = 'storage/val/{}.csv'.format(time.perf_counter_ns())
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
