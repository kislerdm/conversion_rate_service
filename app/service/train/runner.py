# Dmitry Kisler © 2019
# admin@dkisler.com

import os
import time
from typing import Tuple
import pandas as pd
import numpy as np
from service_pkg.logger import getLogger
from service_pkg.file_io import load_data, save_data
import importlib


np.random.seed(2019)

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

MODEL_PKG_NAME = "conversion_rate_model"
MODEL_VERSION = os.getenv("MODEL_VERSION", "v1")

BUCKET_MODEL = "/model"
PREFIX_MODEL = os.getenv("PREFIX_MODEL", 
                         os.path.join(time.strftime('%Y/%m/%d'), 
                                      MODEL_VERSION))

BUCKET_DATA = "/data"

PATH_DATA_TRAIN = os.getenv("PATH_DATA_TRAIN", 
                            os.path.join(time.strftime('%Y/%m/%d'), 
                                         "train.csv.gz"))
PATH_DATA_EVAL = os.getenv("PATH_DATA_EVAL",
                           os.path.join(time.strftime('%Y/%m/%d'),
                                        "eval.csv.gz"))


if __name__ == "__main__":
    logs = getLogger(logger=f"service/train/{MODEL_VERSION}",
                     webhook_url=WEBHOOK_URL)
    
    # link the model module
    try:
        model_definition = importlib.import_module(f"{MODEL_PKG_NAME}.{MODEL_VERSION}.model")
    except Exception as ex:
        logs.send(f"Model {MODEL_VERSION} is not defined in the package {MODEL_PKG_NAME}.\nError:{ex}",
                  lineno=logs.get_line(),
                  kill=True)

    path_data_train = os.path.join(BUCKET_DATA, PATH_DATA_TRAIN)
    if not os.path.isfile(path_data_train):
        logs.send(f"Train data set {path_data_train} not found",
                  lineno=logs.get_line(),
                  kill=True)
    # if no eval data set proveded, use only train data set
    path_data_eval = os.path.join(BUCKET_DATA, PATH_DATA_EVAL)
    if not os.path.isfile(path_data_train):
        path_data_eval = None

    # load data set to train the model
    df, err = load_data(path_data_train)
    if err:
        logs.send(f"Cannot read train data from {path_data_train}. Error:\n{err}",
                  lineno=logs.get_line(),
                  kill=True)

    X, y, err = model_definition.data_preparation(df)
    if err:
        logs.send(f"Train data structure is not aligned with the model requirements. Error:\n{err}",
                  lineno=logs.get_line(),
                  kill=True)
    
    # initilize model
    model = model_definition.Model()
    
    # train the model
    logs.send("Start model training", is_error=False)
    t0 = time.time()
    train_metrics = model.train(X, y)
    t = round(time.time() - t0, 2)
    logs.send(f"Training completed. Elapsed time {t} sec. Model score:\n{train_metrics}", 
              is_error=False, webhook=True)

    # load data set to evaluate the model
    if path_data_eval is not None:
        df_eval, err = load_data(path_data_eval)
        if err:
            logs.send(f"Cannot read eval data from {path_data_eval}."
                      f"Evaluation to be done using train data set. Error:\n{err}",
                      lineno=logs.get_line(),
                      kill=False)
        # model score on evaluation data set
        X_eval, y_eval, err = model_definition.data_preparation(df_eval)
        if err:
            logs.send(f"Eval data set cannot be processed. Error:\n{err}",
                      lineno=logs.get_line())
        else:
            y_eval_pred = model.predict(X_eval)
            eval_metrics = model.score(y_eval, y_eval_pred)
            logs.send(f"Model score on eval data set:\n{eval_metrics}",
                      is_error=False, webhook=True)
    # save the model
    path_model = os.path.join(BUCKET_MODEL, PREFIX_MODEL)
    if not os.path.isdir(path_model):
        os.makedirs(path_model)
    try:
        model.save(path_model)
    except Exception as ex:
        logs.send(f"Cannot save the model to {path_model}. Error:\n{ex}",
                  lineno=logs.get_line(),
                  kill=True)
