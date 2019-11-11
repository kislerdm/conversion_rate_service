# Package with models to predict conversion rate

## Package structure

```
model_pkg
├── conversion_rate_model
│    ├── __init__.py
│    ├── model_template.py <- model definition abstract class
│    ├── v1                <- model version 1
│    │   ├── __init__.py
│    │   ├── model.py
│    │   └── install_dependencies.sh <- OS dependencies installation script
│    └── v2                <- model version 2
│        ├── __init__.py
│        ├── model.py
│        └── install_dependencies.sh
└── test
     ├── test_model_template.py
     ├── v1
     │   └── test_model_v1.py
     └── v2 <- new model's tests
         └── test_model_v2.py
```

Each new model can be added as a submodule to the dir `conversion_rate_model`. The model.py has to include the model definition class `Model` which relies on the abstract class `Model` from `conversion_rate_model/model_template.py`.


## OS dependencies installation

OS dependencies to be specified in `install_dependencies.sh` as `pkgs` argument. For example:

```bash
pkgs='gcc'
```
