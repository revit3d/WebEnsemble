import uuid
import json
import time
import asyncio

import numpy as np

from fastapi import (
    FastAPI, WebSocket, UploadFile, APIRouter,
    WebSocketDisconnect, Form, Depends, File
)
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import get_db
from tasks import fit_model_task
from sockets import connection_manager
import crud
import schemas
import utils

app = FastAPI()
router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@router.post('/model/random_forest')
def create_random_forest(model_params: schemas.RFModelIn,
                         db: Session = Depends(get_db)) -> schemas.RFModelOut:
    """
    Create new record of random forest model in \'ml_models\' table with\\
    passed parameters.

    Parameters:
    -------
    - model_params: random forest model parameters
    - db: database session
    """
    model_db_item = crud.create_model_item(
        db,
        model_type=schemas.ModelType.random_forest,
        model_params=model_params,
    )

    return schemas.RFModelOut(
        uuid=model_db_item.id,
        **json.loads(model_db_item.model_parameters),
    )


@router.post('/model/gradient_boosting')
def create_gradient_boosting(model_params: schemas.GBModelIn,
                             db: Session = Depends(get_db)) -> schemas.GBModelOut:
    """
    Create new record of gradient boosting model in \'ml_models\' table with\\
    passed parameters.

    Parameters:
    -------
    - model_params: gradient boosting model parameters
    - db: database session
    """
    model_db_item = crud.create_model_item(
        db,
        model_type=schemas.ModelType.gradient_boosting,
        model_params=model_params,
    )

    return schemas.GBModelOut(
        uuid=model_db_item.id,
        **json.loads(model_db_item.model_parameters),
    )


@router.put('/model/fit/{uuid_task}')
def put_train_files(uuid_task: uuid.UUID,
                    target_name: str = Form(...),
                    train_file: UploadFile = File(...),
                    val_file: UploadFile | None = File(None),
                    db: Session = Depends(get_db)) -> None:
    """
    Process train and validation data files, save files to the storage\\
    and update record in the corresponding record in \'ml_models\' table.

    Parameters:
    -------
    - uuid_task: uuid of the model to train on the passed data
    - target_name: target column name in passed data
    - train_file: uploaded train file in .csv format
    - val_file: uploaded validation file in .csv format
    - db: database session
    """
    train_data = utils.validate_csv(train_file, target_name)
    val_data = None
    if val_file is not None:
        val_data = utils.validate_csv(val_file, target_name)
    crud.update_model(db, uuid_task, target_name=target_name, train_dataset=train_data, val_dataset=val_data)


@router.websocket('/model/fit')
async def fit_model(websocket: WebSocket,
                    db: Session = Depends(get_db)):
    """
    Fit model on the train data and send notification through the\\
    websocket when the fit finishes and the fitted model is updated\\
    in the \'ml_models\' table.

    Parameters:
    -------
    - websocker: fastapi websocket
    - db: database session
    """
    await connection_manager.connect(websocket)

    try:
        while True:
            uuid_task = await websocket.receive_text()

            # send message about fitting start
            model_db_item = crud.update_model(db, uuid_task, is_trained=False)
            model_status = schemas.ModelStatusElement(
                id=model_db_item.id,
                model_name=model_db_item.model_name,
                is_trained=model_db_item.is_trained,
                target_name=model_db_item.target_name,
            ).model_dump_json()
            await connection_manager.broadcast(model_status)

            fit_task = fit_model_task.delay(uuid_task)

            while not fit_task.ready():
                await asyncio.sleep(1)

            model_status = fit_task.result

            await connection_manager.broadcast(model_status)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)


@router.post('/model/predict/{uuid_task}')
def predict(uuid_task: uuid.UUID,
            test_file: UploadFile = File(...),
            db: Session = Depends(get_db)) -> schemas.PredictInfoOut:
    """
    Predict target for passed data.

    Parameters:
    -------
    - uuid_task: uuid of the trained model
    - test_file: uploaded test file in .csv format
    - db: database session
    """
    # get the model from the database
    model_db_item = crud.read_model_item(db, uuid=uuid_task)
    model = utils.deserialize(model_db_item)['model_deserialized']

    X_test = utils.validate_csv(test_file)
    y_preds = model.predict(X_test.to_numpy())

    preds_file_path = f'storage/predictions/{time.perf_counter_ns()}.csv'
    np.savetxt(preds_file_path, y_preds, delimiter=',')

    return schemas.PredictInfoOut(preds_file_path=preds_file_path)


@router.get('/model/{uuid_task}')
def get_model_info(uuid_task: uuid.UUID,
                   db: Session = Depends(get_db)) -> schemas.RFModelOut | schemas.GBModelOut:
    """
    Return metadata about the model associated with the passed uuid.

    Parameters:
    -------
    - uuid_task: uuid of the model
    - request: fastapi request from the user
    - db: database session
    """
    model_db_item = crud.read_model_item(db, uuid_task)

    model_out_params = utils.deserialize(model_db_item)
    del model_out_params['model_deserialized']

    if model_db_item.model_type is schemas.ModelType.random_forest:
        return schemas.RFModelOut(**model_out_params)
    else:
        return schemas.GBModelOut(**model_out_params)


@router.get('/models/list')
def get_model_names(db: Session = Depends(get_db)) -> schemas.ModelStatuses:
    """Return list with all models' names"""
    model_db_items = crud.read_model_names(db)
    print(model_db_items)
    return schemas.ModelStatuses(models=[
        schemas.ModelStatusElement(
            id=model_db_item.id,
            model_name=model_db_item.model_name,
            is_trained=model_db_item.is_trained,
            target_name=model_db_item.target_name,
        )
        for model_db_item in model_db_items
    ])


app.include_router(router)
