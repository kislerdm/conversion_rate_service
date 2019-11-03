# Dmitry Kisler © 2019
# admin@dkisler.com

import os
import sys
from typing import Tuple, NamedTuple
import pandas as pd
import numpy as np
import pickle
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
import xgboost
import importlib.util

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
            if config is None:
                self.model = xgboost.XGBRegressor()
            else:
                self.model = xgboost.XGBRegressor(**config)

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
    
    def grid_search(self,
                    config: dict,
                    X: pd.DataFrame,
                    y: pd.Series) -> NamedTuple('model_eval',
                                                mse=float):
        """Function for hyper-parameters tuning to search best configuration of the estimator
           Results in the best tuned estimator object being assigned to the Model.model attr
           
           Args:
                config: dictionary with a grid of hyperparameters
                X: pd.DataFrame with features values
                y: target column values

           Returns: 
                namedtuple with metrics values: 
                    "mse": float
        """
        if self.model is None:
            self._model_definition(config=None)
        
        grid = GridSearchCV(self.model,
                            param_grid=config,
                            cv=3,
                            n_jobs=-1,
                            verbose=5)
        # find best tuned estimator
        grid.fit(X, y)
        self.model = grid.best_estimator_
        
        # evalute on train set
        y_pred = self.predict(X)
        model_eval = self.score(y_true=y, y_pred=y_pred)
        return model_eval

    def save(self, path: str):
        """Model saver method

           Args:
                path: path to save model into 
        """
        try:
            with open(os.path.join(path, 'model.pkl'), 'wb') as f:
                f.write(pickle.dumps(self.model))
        except Exception as ex:
            raise ex

    def load(self, path: str):
        """Model loader method

           Args:
                path: path to save model into 
        """
        try:
            with open(path, 'rb') as f:
                self.model = pickle.loads(f.read())
        except Exception as ex:
            raise ex

    def predict(self, X: pd.DataFrame):
        """Predict method

           Args:
                X: pd.DataFrame with features values
        """
        if self.model is None:
            return None
        try:
            return self.model.predict(X)
        except Exception as ex:
            raise ex
            return None
