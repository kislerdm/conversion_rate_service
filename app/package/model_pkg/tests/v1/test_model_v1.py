# Dmitry Kisler © 2019
# admin@dkisler.com

import os
import pytest
from io import StringIO
from pathlib import Path
import importlib.util
from types import ModuleType
import inspect
import pandas as pd
import numpy as np


DIR = Path(os.path.abspath(__file__)).parents[2]

PACKAGE = "conversion_rate_model"
SUFFIX = "v1"
MODULE = "model"

model_methods = ['_model_definition', 'predict',
                 'score', 'model_eval', 
                 'train', 'save', 'load']

model_score = ['mse']

DATASET = """entity_id,device,attrs_scale,att2,att5,att6,att27,att28,att34,cr
5,0,0.5582121675096093,0,1,0,0,0,1,0.0
"""

DATASET = pd.read_csv(StringIO(DATASET))

DATASET_MODEL_COL = [*["device", "attrs_scale"],
                     *[f"att{i}" for i in [2, 5, 6, 27, 28, 34]]]


def load_module(module_name: str) -> ModuleType:
    """Function to load the module.

       Args:
          module_name: module name

       Returns:
          module object
    """
    file_path = os.path.join(DIR, f"{PACKAGE}/{SUFFIX}/{module_name}.py")
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def test_module_exists():
    try:
        _ = load_module(MODULE)
    except Exception as ex:
        raise ex
    return


module = load_module(MODULE)


def test_module_has_model_class():
    assert 'Model' in module.__dir__(), \
        f"Model class is not present in the {MODULE}.py"


def test_model_class_methods():
    model_class_members = inspect.getmembers(module.Model)
    for i in model_methods:
        assert i in str(model_class_members), \
            f"Mothod {i} is not present in the Model class"


def test_module_has_preparation_func():
  assert 'data_preparation' in module.__dir__(), \
      f"data_preparation function is not present in the {MODULE}.py"


def test_model_eval_elements():
    for i in model_score:
        assert getattr(module.Model.model_eval, i), \
            f"Model eval metric {i} is not implemented"


np.random.seed(2019)
model = module.Model()


def test_module_data_preparation():
    X, y, err = module.data_preparation(DATASET)
    print(X.columns)
    if err:
        raise Exception(err)
    assert y[0] == 0, \
        "data_preparation function error"
    missing_columns = list(set(X.columns).difference(DATASET_MODEL_COL))
    assert len(missing_columns) == 0, \
        f"Columns {', '.join(missing_columns)} are not present in the prepared data set"    


def test_define_model():
    model._model_definition()
    assert model is not None, \
        "Model definition error"


def test_train_model():
    X, y, err = module.data_preparation(DATASET)
    if err:
        assert Exception(err)
        
    model_score = model.train(X, y)
    assert model is not None, \
        "Model train error"


def test_save_model():
    try:
        model.save('/tmp')
    except IOError as ex:
        print(f"Cannoe write into /tmp.\nError: {ex}")
    except Exception as ex:
        raise Exception(ex)


def test_load_model():
    path = "/tmp/model.pkl"
    if not os.path.isfile(path):
        return
    try:
        model.load(path)
    except IOError as ex:
        print(f"Cannoe read model from {path}.\nError: {ex}")
    except Exception as ex:
        raise Exception(ex)
    os.remove(path)
