# Dmitry Kisler © 2019
# admin@dkisler.com

from collections import namedtuple
from typing import Tuple, NamedTuple, Any
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from sklearn import metrics
from sklearn.model_selection import train_test_split


def data_preparation(df: pd.DataFrame,
                     target_col='cr',
                     cols_to_drop=[],
                     train_test_ratio=0.3) -> Tuple[pd.DataFrame, 
                                                    pd.DataFrame,
                                                    pd.Series,
                                                    pd.Series, str]:
    """Function to align data with the model requirements

       Args:
            df: input data frame
            target_col: target column name
            cols_to_drop: additional list of columns to drop
            train_test_split: train-test split share

       Returns:
            tuple of the features DataFrame for train, test 
            and target column for train and test, and the error message text            
    """
    try:
        X_train, X_test, y_train, y_test = train_test_split(df.drop([**cols_to_drop, target_col], axis=1),
                                                            df[target_col],
                                                            test_size=train_test_ratio,
                                                            shuffle=True,
                                                            random_state=2019)
        return X_train, X_test, y_train, y_test, None
    except Exception as ex:
        return None, None, None, None, ex
    

class Model(ABC):
    """"Model definition class"""
    model_eval = namedtuple('model_eval', ['mse'])

    def __init__(self,
                 model=None):
        self.model = model
    
    @abstractmethod
    def _model_definition(self, 
                          config: None) -> Any:
        """Function to define and compile the model
        
           Args:
                config: dict with model hyperparameters
           
           Returns:
                model object
        """
        pass
    
    @abstractmethod    
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
        
        # train step
        
        # eval step
        y_pred = None
        model_eval = self.score(y_true=y, y_pred=y_pred)
        return model_eval

    @classmethod
    def score(cls,
              y_true: np.array,
              y_pred: np.array) -> NamedTuple('model_eval',
                                              mse=float):
        """Model metrics evaluation

           Args:
                y_true: true values vector
                y_pred: predicted values vector

           Returns:
                namedtuple with metrics values: 
                    "mse": float
        """
        return cls.model_eval(mse=metrics.mean_squared_error(y_true, y_pred))

    @abstractmethod
    def save(self, path: str):
        """Model saver method

           Args:
                path: path to save model into 
        """
        pass
    
    @abstractmethod    
    def load(self, path: str):
        """Model loader method

           Args:
                path: path to save model into 
        """
        pass
    
    @abstractmethod    
    def predict(self, X: pd.DataFrame):
        """Predict method

           Args:
                X: pd.DataFrame with features values
        """
        if self.model is None:
            return None
        pass
