# Dmitry Kisler © 2019
# www.dkisler.com

import pandas as pd
import pickle
from typing import Tuple


def load_data(path: str) -> Tuple[pd.DataFrame, str]:
    """Function to load data set for prediction

       Args:
          path: path to data

       Returns:
          tuple with the data set DataFrame and error string
    """
    try:
        df = pd.read_csv(path)
        return df, None
    except Exception as ex:
        return None, ex


def save_data(df: pd.DataFrame, path: str):
    """Function to save model predictions

       Args:
          df: data set with prediction results
          path: path to store data into
    """
    try:
        df.to_csv(path,
                  compression='gzip',
                  index=False)
    except IOError as ex:
        raise ex


def load_data_pkl(path: str) -> Tuple[pd.DataFrame, str]:
    """Function to load and deserialize data set from pickled file

       Args:
          path: path to data

       Returns:
          tuple with the data set DataFrame and error string
    """
    try:
        with open(path, 'rb') as f:
            df = pickle.load(f)
        return df, None
    except Exception as ex:
        return None, ex


def save_data_pkl(df: pd.DataFrame, path: str):
    """Function to serialize and save data set as pickled files

       Args:
          df: data set with prediction results
          path: path to data

       Returns:
          tuple with the data set DataFrame and error string
    """
    try:
        with open(path, 'wb') as f:
            pickle.dump(df, f)
    except IOError as ex:
        raise ex
