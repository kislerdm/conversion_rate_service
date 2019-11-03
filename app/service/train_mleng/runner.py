import os
import sys
import time
import yaml
from typing import Tuple
import pandas as pd
import numpy as np
import argparse
from google.cloud import storage
from service_pkg.logger import getLogger
from service_pkg.file_io import load_data_pkl, load_data
import importlib
from pathlib import Path


np.random.seed(2019)

DIR = str(Path(os.path.abspath(__file__)).parents[0])
SERVICE_NAME = str(Path(os.path.abspath(__file__)).parents[2])
if SERVICE_NAME in DIR:
  SERVICE_NAME = DIR.replace(SERVICE_NAME, '')[1:]


def get_args():
    """Argument parser.
    Returns:
      Dictionary of arguments.
    """
    parser = argparse.ArgumentParser(description='cr prediction train')
    parser.add_argument(
        '--data-path',
        default=None,
        required=True,
        help='Path to data sample')
    parser.add_argument(
        '--config-path',
        default=None,
        required=False,
        help='Path to the config file')
    parser.add_argument(
        '--model-dir',
        default=None,
        required=False,
        help='The directory to store the model')
    parser.add_argument(
        '--validation-split',
        type=float,
        default=0.3,
        required=False,
        help='Input batch size for testing (default: 0.3)')
    parser.add_argument(
        '--seed',
        type=int,
        default=2019,
        required=False,
        help='Random seed (default: 2019)')
    parser.add_argument(
        '--webhook-url',
        type=str,
        default=None,
        required=False,
        help='Url to push webhook to')

    args = parser.parse_args()
    return args
  

MODEL_PKG_NAME = "conversion_rate_model"
MODEL_VERSION = os.getenv("MODEL_VERSION")
if MODEL_VERSION is None:
  MODEL_VERSION = "v1"

BUCKET_DATA = os.getenv("BUCKET_DATA")
if BUCKET_DATA is None:
  BUCKET_DATA = "/data"

BUCKET_CONFIG = os.getenv("BUCKET_CONFIG")
if BUCKET_CONFIG is None:
  BUCKET_CONFIG = "/config"

BUCKET_MODEL = os.getenv("BUCKET_MODEL")
if BUCKET_MODEL is None:
  BUCKET_MODEL = "/model"


def is_gs_bucket(bucket: str) -> Tuple[bool, str]:
    """Function to check if the bucket exists
       
       Args:
          bucket: gs bucket name
       
       Returns:
          tuple with boolean flag and error (in case of exception)
    """
    # ckeck if bucket exists
    try:
        buckets_list = [i.id for i in list(gs.list_buckets())
                        if i.id == bucket]
    except Exception as ex:
        return False, f"Cannot list buckets. Error:\n{ex}"

    if len(buckets_list) == 0:
        return False, f"Bucket '{bucket}' doesn't exist"
    
    return True, None
  
  
def is_gs_file(bucket: str, 
               obj: str) -> Tuple[bool, str]:
    """Function to check if the object exists
    
       Args:
          bucket: gs bucket name
          obj: object path
       
       Returns:
          tuple with boolean flag and error (in case of exception)
    """
    is_bucket, err = is_gs_bucket(bucket)
    if err:
      return False, err

    # check if the object exists in the bucket
    try:
        bucket_objects = gs.list_blobs(bucket)
        bucket_object = [i.name for i in list(bucket_objects)
                         if i.name == obj]
    except Exception as ex:
      return False, f"Cannot list bucket files. Error:\n{ex}"

    if len(bucket_object) == 0:
      return False, "Query '{obj}' doesn't exist"

    return True, None


if __name__ == "__main__":
    args = get_args()
    WEBHOOK_URL = args.webhook_url
    
    logs = getLogger(f"{SERVICE_NAME}/{MODEL_VERSION}",
                     webhook_url=WEBHOOK_URL)
    
    PATH_DATA = args.data_path

    PATH_CONFIG = args.config_path
    if PATH_CONFIG is None:
        PATH_CONFIG = os.path.join(MODEL_VERSION, "config.yaml")
    
    PATH_MODEL = args.model_dir
    if PATH_MODEL is None:
        PATH_MODEL = os.path.join(MODEL_VERSION,
                                  time.strftime('%Y/%m/%d'))
    
    # link the model module
    try:
        model_pkg = importlib.import_module(
            f"{MODEL_PKG_NAME}.{MODEL_VERSION}.model")
    except Exception as ex:
        logs.send(f"Model {MODEL_VERSION} is not defined in the package {MODEL_PKG_NAME}.\nError:{ex}",
                  lineno=logs.get_line(),
                  kill=True)
    
    # get gs client (this step can be modified to access s3 bucket)
    try:
        gs = storage.Client()
    except Exception as ex:
      logs.send(f"Cannot connect to GS. Error:\n{ex}", 
                lineno=logs.get_line(),
                kill=True)
    
    # check if specified buckets exist
    for bucket in [BUCKET_DATA, BUCKET_CONFIG, BUCKET_MODEL]:
      flag, err = is_gs_bucket(bucket)
      if err:
        logs.send(err, 
                  lineno=logs.get_line(), 
                  kill=True)
    
    # check if data exist
    flag, err = is_gs_file(bucket=BUCKET_DATA, obj=PATH_DATA)
    if err:
      logs.send(err, 
                lineno=logs.get_line(), 
                kill=True)

    # download the train data set
    df, err = load_data_pkl(os.path.join(BUCKET_DATA, PATH_DATA))
    if err:
      logs.send(err,
                lineno=logs.get_line(),
                kill=True)
    
    # prepare data for training
    X_train, X_test, y_train, y_test, err = model_pkg.data_preparation(df)
    if err:
      logs.send(err,
                lineno=logs.get_line(),
                kill=True)
    
    # instantiate a model class object
    model = model_pkg.Model()
    
    # read the config in case it's provided
    t0 = time.time()
    if PATH_CONFIG:
      logs.send("Start training with grid search",
                is_error=False,
                kill=False)
      try:
        config_test = gs.get_bucket(BUCKET_CONFIG)\
                      .get_blob(PATH_CONFIG)\
                      .download_as_string()

        config = yaml.safe_load(config_test)
      except Exception as ex:
        logs.send(ex,
                  lineno=logs.get_line(),
                  kill=True)
      
      metrics_train = model.grid_search(X=X_train,
                                        y=y_train,
                                        config=config)
    else:
      logs.send("Start training",
                is_error=False,
                kill=False)
      
      metrics_train = model.train(X=X_train,
                                  y=y_train)
    
    t = round(time.time() - t0, 2)
    logs.send(f"Training completed. Elapsed time: {t} sec.\nModel performance: {metrics_train}",
              is_error=False,
              kill=False, 
              webhook=True)

    # evaluate model on test data set
    try:
      metrics_eval = model.score(y_test, model.predict(X_test))
    except Exception as ex:
      logs.send(f"Model evaluation error: {ex}",
                lineno=logs.get_line(),
                kill=True)
    
    logs.send(f"Model eval performance: {metrics_eval}",
              is_error=False,
              kill=False,
              webhook=True)
    
    # save the model
    tmp_model_dir = f"/tmp/{MODEL_VERSION}"
    dest_model_dir = os.path.join(BUCKET_MODEL, args.model_dir)
    model.save(tmp_model_dir)
    try:
        os.system(f"gsutil cp -r {tmp_model_dir}/* {dest_model_dir}")
    except Exception as ex:
        logs.send(f"Cannot copy from '{tmp_model_dir}' to '{dest_model_dir}'. Error:\n{ex}",
                  lineno=logs.get_line(),
                  kill=True)
    
    logs.send(f"Model saved to {dest_model_dir}.",
              is_error=False,
              kill=False,
              webhook=True)
