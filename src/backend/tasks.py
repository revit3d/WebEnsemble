from fastapi import WebSocket
from worker import celery
from sqlalchemy.orm import Session

import pandas as pd

from ensembles import RandomForestMSE, GradientBoostingMSE
import schemas
import crud


@celery.task
async def fit_model_task(model_item_deserialized: dict, websocket: WebSocket, db: Session):
    ensemble_params = model_item_deserialized['ensemble_params']
    tree_params = model_item_deserialized['tree_params']
    target_name = model_item_deserialized['target_name']
    uuid_task = model_item_deserialized['uuid']
    model_name = model_item_deserialized['model_name']

    if model_name is schemas.ModelName.random_forest:
        model = RandomForestMSE(
            **ensemble_params,
            **tree_params,
        )
    else:
        model = GradientBoostingMSE(
            **ensemble_params,
            **tree_params,
        )

    # parse train data
    train_data = pd.read_csv(model_item_deserialized['train_dataset_file_path'])
    X_train, y_train = train_data.drop(target_name, axis=1), train_data[target_name]

    # parse val data if present
    X_val, y_val = None, None
    if model_item_deserialized['val_dataset_file_path'] is not None:
        val_data = pd.read_csv(model_item_deserialized['val_dataset_file_path'])
        X_val, y_val = val_data.drop(target_name, axis=1), val_data[target_name]

    # fit the model and save it to the database
    train_loss, val_loss = model.fit(X_train, y_train, X_val, y_val)
    crud.update_model(db, uuid_task, model, train_loss, val_loss)

    await websocket.send_text('model {} fit finished'.format(uuid_task))
