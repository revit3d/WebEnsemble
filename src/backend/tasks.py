import pandas as pd

from worker import celery
from ensembles import RandomForestMSE, GradientBoostingMSE
import schemas


@celery.task
def fit_model_task(model_item_deserialized: dict):
    """
    Celery task for fitting the model.

    Parameters:
    -------
    - model_item_deserialized: deserialized record from the \'ml_models\' table
    """
    ensemble_params = model_item_deserialized['ensemble_params']
    tree_params = model_item_deserialized['tree_params']
    target_name = model_item_deserialized['target_name']
    model_type = model_item_deserialized['model_type']

    if model_type == schemas.ModelType.random_forest:
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
    X_train = train_data.drop(target_name, axis=1).to_numpy()
    y_train = train_data[target_name].to_numpy()

    # parse val data if present
    X_val, y_val = None, None
    if model_item_deserialized['val_dataset_file_path'] is not None:
        val_data = pd.read_csv(model_item_deserialized['val_dataset_file_path'])
        X_val = val_data.drop(target_name, axis=1).to_numpy()
        y_val = val_data[target_name].to_numpy()

    # fit the model and save it to the database
    train_loss, val_loss = model.fit(X_train, y_train, X_val, y_val)
    return model, train_loss, val_loss
