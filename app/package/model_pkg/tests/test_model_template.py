# Dmitry Kisler © 2019
# www.dkisler.com

import os
import importlib.util
from types import ModuleType
import pytest
import inspect

DIR = os.path.dirname(os.path.abspath(__file__))

PACKAGE = "conversion_rate_model"
MODULE = "model_template"

model_methods = ['_model_definition', 'predict', 
                 'score', 'model_eval',
                 'train', 'save', 'load']

model_score = ['mse']


def load_module(module_name: str) -> ModuleType:
    """Function to load the module.

       Args:
          module_name: module name

       Returns:
          module object
    """
    file_path = os.path.join(os.path.dirname(
        DIR), f"{PACKAGE}/{module_name}.py")
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


def test_module_has_preparation_func():
  assert 'data_preparation' in module.__dir__(), \
      f"data_preparation function is not present in the {MODULE}.py"
  return


def test_model_class_methods():
    model_class_members = inspect.getmembers(module.Model)
    for i in model_methods:
      assert i in str(model_class_members), \
        f"Mothod {i} is not present in the Model class"
        

def test_model_eval_elements():
    for i in model_score:
        assert getattr(module.Model.model_eval, i), \
          f"Model eval metric {i} is not implemented"
