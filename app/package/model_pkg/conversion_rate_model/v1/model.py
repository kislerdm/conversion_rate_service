# Dmitry Kisler © 2019
# www.dkisler.com

import os
from typing import Tuple, NamedTuple
import pandas as pd
import numpy as np
import pickle
from sklearn import metrics
from sklearn.linear_model import LinearRegression
import importlib.util
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# import model abstract class
module_name = "model_template"
file_path = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))),
    f"{module_name}.py")
spec = importlib.util.spec_from_file_location(module_name, file_path)
model_template = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model_template)


data_preparation = model_template.data_preparation


class Model(model_template.Model):
    """"Model definition class"""

    def __init__(self,
                 model=None):
        self.model = model

    def _model_definition(self,
                          config=None):
        """Function to define and compile the model

        Args:
            config: dict with model hyperparameters

        Returns:
            model object
        """
        if self.model is None:
            self.model = LinearRegression()

    def train(self,
              X: pd.DataFrame,
              y: pd.Series) -> NamedTuple('model_eval',
                                          mse=float):
        """Train method

        Args:
            X: pd.DataFrame with features values
            y: target column values

        Returns: 
            namedtuple with metrics values: 
                "mse": float
        """
        if self.model is None:
            self._model_definition()

        self.model.fit(X, y)
        # evalute on train set
        y_pred = self.predict(X)
        model_eval = self.score(y_true=y, y_pred=y_pred)
        return model_eval

    def save(self, path: str):
        """Model saver method

        Args:
            path: path to save model into

        Raises:
            IOError, save error
        """
        try:
            if not os.path.isdir(path):
                os.makedirs(path)
            with open(os.path.join(path, 'model.pkl'), 'wb') as f:
                pickle.dump(self.model, f)
        except Exception as ex:
            raise ex

    def load(self, path: str):
        """Model loader method

        Args:
            path: path to save model into

        Raises:
            IOError, load error
        """
        try:
            with open(path, 'rb') as f:
                self.model = pickle.load(f)
        except Exception as ex:
            raise ex

    def predict(self, X: pd.DataFrame) -> pd.Series:
        """Predict method

        Args:
            X: pd.DataFrame with features values

        Raises:
            Prediction error
        """
        if self.model is None:
            return None
        try:
            return self.model.predict(X)
        except Exception as ex:
            raise ex
            return None
