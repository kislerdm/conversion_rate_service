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
                 'train', 'grid_search',
                 'save', 'load']

model_score = ['mse']

# TODO: add train dataset sample
DATASET = """"att1","att2","att3","att4","att5","att6","att7","att8","att9","att10","att11","att12","att13","att14","att15","att16","att17","att18","att19","att20","att21","att22","att23","att24","att26","att27","att28","att29","att30","att31","att32","att33","att34","att36","att37","att38","att39","att40","att41","att42","att43","att44","att45","att46","att47","att48","att49","att50","att51","att52","att53","att54","att55","att56","att57","att58","att59","att60","att61","att62","att63","att64","att65","att66","att67","att68","att69","att70","att71","att72","att73","att74","att75","att76","att77","att78","att79","att80","att81","att82","att83","att84","att85","att86","att87","att88","att89","att90","att91","att92","att93","att94","att95","att96","att97","att98","att99","att100","att101","att102","att103","att104","att105","att106","att107","att108","att109","att110","att111","att112","att113","att114","att115","att116","att117","att118","att119","att120","att121","att122","att123","att124","att125","att126","att127","att128","att129","att130","att131","att132","att133","att134","att135","att136","att137","att138","att139","att140","att141","att142","att143","att144","att145","att146","att147","att148","att149","att150","att151","att152","att153","att154","att155","att156","att157","att158","att159","att160","cr"
1,0,1,0,1,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0.0
1,0,1,0,1,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0.0
1,0,1,0,1,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0.0
1,0,1,0,1,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.5
"""

DATASET = pd.read_csv(StringIO(DATASET))

DATASET_MODEL_COL = [f"att{i}" for i in range(1, 160, 1)
                     if i not in [26, 35]]
DATASET_MODEL_COL.append('cr')


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
    return


def test_model_class_methods():
    model_class_members = inspect.getmembers(module.Model)
    for i in model_methods:
        assert i in str(model_class_members), \
            f"Mothod {i} is not present in the Model class"


def test_module_has_preparation_func():
  assert 'data_preparation' in module.__dir__(), \
      f"data_preparation function is not present in the {MODULE}.py"
  return


def test_model_eval_elements():
    for i in model_score:
        assert getattr(module.Model.model_eval, i), \
            f"Model eval metric {i} is not implemented"


np.random.seed(2019)
model = module.Model()


def test_module_data_preparation():
    X_train, X_test,\
        y_train, y_test, err = module.data_preparation(DATASET)
    assert err is None, \
        f"Data prep error: {err}"  


def test_define_model():
    model._model_definition()
    assert model is not None, \
        "Model definition error"


def test_train_model():
    pass


def test_grid_search():
    pass


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
