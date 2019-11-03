# Conversion Rate Prediction Service


Objectives:

![sellics_logo](https://sellics.com/wp-content/uploads/2018/02/sellics-fb.jpg)

### Model re-train

GCP ML Engine is being used for faster model experimentation and retraining:

1. Build a generic service
2. Add model to the model_pkg
3. Build a train image
4. Push the image container to the google container registry (gcr)
5. Push a set of hyper-parameters to google cloud storage bucket (gs)
6. Trigger a training job

Infra:

```yaml
- GS:
  - 
```