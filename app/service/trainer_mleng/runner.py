import os
import time
import pandas as pd
import numpy as np
import argparse
import yaml
from service_pkg.logger import getLogger
from service_pkg.file_io import load_data_pkl
from google.cloud import bucket

np.random.seed(2019)


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
  

MODEL_PKG_NAME = "recipe_score_model"

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


if __name__ == "__main__":
  
    args = get_args()
    
    PATH_DATA = args['data_path']

    PATH_MODEL = args['model_dir']
    if PATH_MODEL is None:
        PATH_MODEL = os.path.join(MODEL_VERSION,
                                  time.strftime('%Y/%m/%d'))
    
    PATH_CONFIG = args['config_path']
    if PATH_CONFIG is None:
        PATH_CONFIG = os.path.join(MODEL_VERSION, "config.yaml")
        
    WEBHOOK_URL = args['webhook_url']
    
    logs = getLogger(f"service/trainer/mleng/{MODEL_VERSION}", 
                     webhook_url=WEBHOOK_URL)
    
    
    
    
