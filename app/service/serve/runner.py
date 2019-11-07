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


WEBHOOK_URL = os.getenv("WEBHOOK_URL")

MODEL_PKG_NAME = "conversion_rate_model"
MODEL_VERSION = os.getenv("MODEL_VERSION", "v0")

BUCKET_MODEL = "/model"
PATH_MODEL = os.getenv("PATH_MODEL", 
                       os.path.join(MODEL_VERSION, 
                                    time.strftime('%Y/%m/%d'),
                                    'model.pkl'))

BUCKET_DATA = "/data"
PATH_DATA_IN = os.getenv("PATH_DATA_IN", 
                         os.path.join("input",
                                      time.strftime('%Y/%m/%d'),
                                      "predict_input.csv.gz"))

PATH_DATA_OUT = os.getenv("PATH_DATA_OUT",
                          os.path.join("output",
                                       time.strftime('%Y/%m/%d'),
                                       "predict_output.csv.gz"))

COL_ID = "entity_id"


if __name__ == "__main__":

    logs = getLogger(logger=f"service/serve/{MODEL_VERSION}",
                     webhook_url=WEBHOOK_URL)

    # link the model module
    try:
        model_definition = importlib.import_module(f"{MODEL_PKG_NAME}.{MODEL_VERSION}.model")
    except Exception as ex:
        logs.send(f"Model {MODEL_VERSION} is not defined in the package {MODEL_PKG_NAME}.\nError:{ex}",
                  lineno=logs.get_line(),
                  kill=True)

    path_data_in = os.path.join(BUCKET_DATA, PATH_DATA_IN)
    if not os.path.isfile(path_data_in):
        logs.send(f"Data file(s) {path_data_in} not found",
                  lineno=logs.get_line(),
                  kill=True)

    path_model = os.path.join(BUCKET_MODEL, PATH_MODEL)
    if not os.path.isfile(path_model):
        logs.send(f"Model {path_model} not found",
                  lineno=logs.get_line(),
                  kill=True)

    # instantiate the model object
    model = model_definition.Model()
    try:
        model.load(path_model)
    except Exception as ex:
        logs.send(f"Cannot load model from {path_model}. Error:\n{ex}",
                  lineno=logs.get_line(),
                  kill=True)

    # load data set to feed into the model
    df, err = load_data(path_data_in)
    if err:
        logs.send(f"Cannot read data from {path_data_in}. Error:\n{err}",
                  lineno=logs.get_line(),
                  kill=True)

    X, y, err = model_definition.data_preparation(df, target=None)
    if err:
        logs.send(f"Input data structure is not aligned with the model requirements. Error:\n{err}",
                  lineno=logs.get_line(),
                  kill=True)

    # run prediction
    t0 = time.time()
    try:
        prediction_results = model.predict(X)
        t = round(time.time() - t0, 2)
        logs.send(f"Prediction completed. Elapsed time: {t} sec. Saving results.", 
                  is_error=False)
    except Exception as ex:
        logs.send(f"Prediction error.\n{ex}",
                  lineno=logs.get_line(),
                  kill=True)

    # convert results to comply with the output SLA
    try:
        df_prediction_results = pd.DataFrame({
            eval(COL_ID): df[COL_ID]
            })
        df_prediction_results.append(prediction_results)
    except Exception as ex:
        logs.send(f"Cannot convert prediction according to output SLA. Error:\n{ex}",
                  lineno=logs.get_line(),
                  kill=True)

    path_data_out = os.path.join(BUCKET_DATA, PATH_DATA_OUT)
    if not os.path.isdir(os.path.dirname(path_data_out)):
        os.makedirs(os.path.dirname(path_data_out))
    try:
        save_data(df_prediction_results, path=path_data_out)
    except Exception as ex:
        logs.send(f"Cannot save prediction into {path_data_out}. Error:\n{ex}",
                  lineno=logs.get_line(),
                  kill=True)
        
    t = round(time.time() - t0, 2)
    logs.send(f"Serve service successfully completed. Total Elapsed time: {t} sec.", 
              is_error=False, 
              webhook=True)
