import uuid
import json

from fastapi import FastAPI, WebSocket, UploadFile, Depends, File
from sqlalchemy.orm import Session

from schemas import *
from database import get_db
from tasks import fit_model_task
import crud
import utils

app = FastAPI()


@app.post('/model/random_forest')
def create_random_forest(model_params: RFModelIn,
                         db: Session = Depends(get_db)) -> RFModelOut:
    model_db_item = crud.create_model_item(
        db,
        model_name=ModelName.random_forest,
        model_params=model_params,
    )

    return RFModelOut(
        uuid=model_db_item.id,
        **json.loads(model_db_item.model_parameters),
    )


@app.post('/model/gradient_boosting')
def create_gradient_boosting(model_params: RFModelIn,
                             db: Session = Depends(get_db)) -> GBModelOut:
    model_db_item = crud.create_model_item(
        db,
        model_name=ModelName.gradient_boosting,
        model_params=model_params,
    )

    return GBModelOut(
        uuid=model_db_item.id,
        **json.loads(model_db_item.model_parameters),
    )


@app.put('/model/fit/{uuid_task}')
def fit_model(uuid_task: uuid.UUID,
              target_name: str,
              train_file: UploadFile = File(...),
              val_file: UploadFile | None = File(None),
              db: Session = Depends(get_db)) -> None:
    train_data = utils.validate_csv(train_file, target_name)
    val_data = None
    if val_file is not None:
        val_data = utils.validate_csv(val_file, target_name)
    crud.update_model(db, uuid_task, target_name=target_name, train_dataset=train_data, val_dataset=val_data)


@app.websocket('/model/fit')
async def fit_model(websocket: WebSocket,
                    db: Session = Depends(get_db)):
    await websocket.accept()

    while True:
        uuid_task = await websocket.receive_text()

        model_db_item = crud.read_model(db, id=uuid_task)
        model_item_deserialized = utils.deserialize(model_db_item)
        fit_model_task.delay(model_item_deserialized)


@app.get('/model/predict/{uuid_task}')
def predict(uuid_task: uuid.UUID,
            test_dataset: UploadFile = File(...),
            db: Session = Depends(get_db)) -> PredictInfoOut:
    # get the model from the database
    model_db_item = crud.read_model(db, id=uuid_task)
    model = utils.deserialize(model_db_item)['model_deserialized']

    X_test = utils.read_csv(test_dataset)
    y_preds = model.predict(X_test)

    return PredictInfoOut(y_preds=y_preds)


@app.get('/model/{uuid_task}')
def get_model_info(uuid_task: uuid.UUID,
                   db: Session = Depends(get_db)) -> RFModelOut | GBModelOut:
    model_db_item = crud.read_model(db, uuid_task)

    model_out_params = utils.deserialize(model_db_item)
    del model_out_params['model_deserialized']

    if model_db_item.model_name is ModelName.random_forest:
        return RFModelOut(**model_out_params)
    else:
        return GBModelOut(**model_out_params)
    

@app.get("/convert/{file_path}")
async def convert_file_path(file_path: str):
    http_url = utils.convert_to_http_url(file_path)
    return {"file_path": file_path, "http_url": http_url}
