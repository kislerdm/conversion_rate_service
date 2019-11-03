# Package with models to predict conversion rate

## Package structure

```bash
conversion_rate_model
├── __init__.py
├── model_template.py <- model definition abstract class
├── v1                <- model version 1
│    ├── __init__.py
│    └── model.py
└── v2                <- model version 2
    ├── __init__.py
    └── model.py
```

Each new model can be added as a submodule to the dir `conversion_rate_model`. The model.py has to include the model definition class `Model` which relies on the abstract class `Model` from `conversion_rate_model/model_template.py`.