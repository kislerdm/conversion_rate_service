#! /bin/sh

VERSION=$1
PROJECT_ID=sellics
REGION=us-central1


platforms=(computer smartphone tablet)
for platform in ${platforms[@]}; do
  JOB_NAME=${PROJECT_ID}_${platform}_$(TZ=":UTC" date +%Y%m%dT%H%M%SZ)

  gcloud ai-platform jobs submit training ${JOB_NAME} \
    --master-image-uri gcr.io/${PROJECT_ID}/service/trainer:${VERSION} \
    --region ${REGION} \
    --config config.yaml \
    -- \
    --data-path=train/${VERSION}/data_${platform}.pkl \
    --config-path=${VERSION}/params.yaml \
    --model-dir=${VERSION}/${platform}/$(TZ=":UTC" date +%Y/%m/%d/%H)
done