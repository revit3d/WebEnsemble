import uuid
import json

from fastapi import FastAPI, WebSocket, UploadFile, Request, Depends, File
from sqlalchemy.orm import Session

from schemas import RFModelIn, GBModelIn, ModelName, RFModelOut, GBModelOut, PredictInfoOut
from database import get_db
from tasks import fit_model_task
import crud
import utils

app = FastAPI()


@app.post('/model/random_forest')
def create_random_forest(model_params: RFModelIn,
                         db: Session = Depends(get_db)) -> RFModelOut:
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
        model_name=ModelName.random_forest,
        model_params=model_params,
    )

    return RFModelOut(
        uuid=model_db_item.id,
        **json.loads(model_db_item.model_parameters),
    )


@app.post('/model/gradient_boosting')
def create_gradient_boosting(model_params: GBModelIn,
                             db: Session = Depends(get_db)) -> GBModelOut:
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
        model_name=ModelName.gradient_boosting,
        model_params=model_params,
    )

    return GBModelOut(
        uuid=model_db_item.id,
        **json.loads(model_db_item.model_parameters),
    )


@app.put('/model/fit/{uuid_task}')
def put_train_files(uuid_task: uuid.UUID,
                    target_name: str,
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


@app.websocket('/model/fit')
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
    await websocket.accept()

    while True:
        uuid_task = await websocket.receive_text()

        model_db_item = crud.read_model_item(db, uuid=uuid_task)
        model_item_deserialized = utils.deserialize(model_db_item)
        fit_results = fit_model_task.delay(model_item_deserialized)
        model, train_loss, val_loss = fit_results.get()
        crud.update_model(db, uuid_task, model=model, train_loss=train_loss, val_loss=val_loss)
        await websocket.send_text(f'model {uuid_task} fit finished')


@app.post('/model/predict/{uuid_task}')
def predict(uuid_task: uuid.UUID,
            test_file: UploadFile = File(...),
            db: Session = Depends(get_db)) -> PredictInfoOut:
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

    return PredictInfoOut(y_preds=y_preds)


@app.get('/model/{uuid_task}')
def get_model_info(uuid_task: uuid.UUID,
                   request: Request,
                   db: Session = Depends(get_db)) -> RFModelOut | GBModelOut:
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

    model_out_params['train_dataset_file_path'] = utils.convert_to_http_url(
        request,
        model_out_params['train_dataset_file_path']
    )
    if model_out_params['val_dataset_file_path'] is not None:
        model_out_params['val_dataset_file_path'] = utils.convert_to_http_url(
            request,
            model_out_params['val_dataset_file_path']
        )

    if model_db_item.model_name is ModelName.random_forest:
        return RFModelOut(**model_out_params)
    else:
        return GBModelOut(**model_out_params)
