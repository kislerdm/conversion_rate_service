#! /bin/sh

VERSION=$1
PROJECT_ID=sellics
REGION=us-central1

JOB_NAME=${PROJECT_ID}_$(TZ=":UTC" date +%Y%m%dT%H%M%SZ)

gcloud ai-platform jobs submit training ${JOB_NAME} \
  --master-image-uri gcr.io/${PROJECT_ID}/service/trainer:${VERSION} \
  --region ${REGION} \
  --config config.yaml \
  -- \
  --data-path=train/${VERSION}/data_computer.pkl \
  --config-path=${VERSION}/params_test.yaml \
  --model-dir=${VERSION}/$(TZ=":UTC" date +%Y/%m/%d/%H)