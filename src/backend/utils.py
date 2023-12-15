import json
import pickle

import pandas as pd
import numpy as np

from fastapi import UploadFile, HTTPException

import models


def validate_csv(file: UploadFile, target_name=None) -> pd.DataFrame:
    """
    Validates a csv file, uploaded via fastapi. Checks, that the file\\
    can be opened and read by pandas, and checks if the target exists\\
    in file, if target name is passed.

    Parameters:
    -------
    - file: a .csv file to validate
    - target_name: target column name to look for. If column with such name\\
    is not found, an exception is raised
    """
    try:
        data = pd.read_csv(file.file)
        file.file.close()
        if target_name is not None:
            _ = data[target_name]
    except (pd.errors.ParserError, KeyError) as exc:
        raise HTTPException(422, detail=f'Bad file format for file {file.filename}') from exc

    return data


def deserialize(model_db_item: models.MLModel):
    """
    Deserializes a record from the \'ml_models\' table.

    Parameters:
    -------
    - model_db_item: a single-row result of a query to the\\
    \'ml_models\' table
    """
    model_deserialized = None
    train_loss_deserialized = None
    val_loss_deserialized = None
    if model_db_item.model_serialized is not None:
        model_deserialized = pickle.loads(model_db_item.model_serialized)
        if model_db_item.train_loss is not None:
            train_loss_deserialized = np.frombuffer(model_db_item.train_loss)
        if model_db_item.val_loss is not None:
            val_loss_deserialized = np.frombuffer(model_db_item.val_loss)

    model_out_params = {
        'uuid': model_db_item.id,
        'model_name': model_db_item.model_name,
        'model_type': model_db_item.model_type,
        **json.loads(model_db_item.model_parameters),
        'is_trained': model_db_item.is_trained,
        'model_deserialized': model_deserialized,
        'train_dataset_file_path': model_db_item.train_dataset_file_path,
        'val_dataset_file_path': model_db_item.val_dataset_file_path,
        'train_loss': train_loss_deserialized,
        'val_loss': val_loss_deserialized,
        'target_name': model_db_item.target_name,
    }

    return model_out_params
