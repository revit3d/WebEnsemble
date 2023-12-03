import os
import json
import pickle

import pandas as pd
import numpy as np

from fastapi import UploadFile, HTTPException
from pydantic import HttpUrl

import models

def validate_csv(file: UploadFile, target_name) -> pd.DataFrame:
    try:
        data = pd.read_csv(file.file)
        file.file.close()
        data[target_name]
    except pd.errors.ParserError or KeyError:
        HTTPException(422, detail='Bad file format for file {}'.format(file.filename))
    return data


def deserialize(model_db_item: models.MLModel):
    if model_db_item.model_serialized is not None:
        model_deserialized = pickle.loads(model_db_item.model_serialized)
        if model_db_item.train_loss is not None:
            train_loss_deserialized = np.frombuffer(model_db_item.train_loss)
        if model_db_item.val_loss is not None:
            val_loss_deserialized = np.frombuffer(model_db_item.val_loss)

    model_out_params = {
        'uuid': model_db_item.id,
        **json.loads(model_db_item.model_parameters),
        'model_deserialized': model_deserialized,
        'train_loss': train_loss_deserialized,
        'val_loss': val_loss_deserialized,
        'train_dataset_file_path': model_db_item.train_dataset_file_path,
        'val_dataset_file_path': model_db_item.val_dataset_file_path,
    }

    return model_out_params


def convert_to_http_url(file_path: str) -> HttpUrl:
    # Get the absolute path of the file
    absolute_file_path = os.path.abspath(file_path)

    # Assuming the file is served from the root path "/"
    return HttpUrl(f"file:///{absolute_file_path}")