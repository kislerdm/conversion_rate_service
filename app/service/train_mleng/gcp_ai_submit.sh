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
  --config-path=${VERSION}/params.yaml \
  --model-dir=${VERSION} \
  --webhook-url="https://hooks.slack.com/services/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"