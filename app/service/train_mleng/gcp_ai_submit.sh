#! /bin/bash

docker run \
-v ${PWD}/gcp-key.json:/credentials.json \
-e GOOGLE_APPLICATION_CREDENTIALS=/credentials.json \
-t service/train-mleng:v1 \
--data-path=train/v1/data_computer.pkl \
--config-path=v1/params.yaml \
--model-dir=v1/model_computer.pkl \
--webhook-url="https://hooks.slack.com/services/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"