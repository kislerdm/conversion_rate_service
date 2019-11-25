#! /bin/sh

VERSION=$1
PROJECT_ID=cr_model
REGION=us-central1
PARAMS=params_v2

platforms=(computer smartphone tablet)
for platform in ${platforms[@]}; do
  JOB_NAME=${PROJECT_ID}_${platform}_$(TZ=":UTC" date +%Y%m%dT%H%M%SZ)

  gcloud ai-platform jobs submit training ${JOB_NAME} \
    --master-image-uri gcr.io/${PROJECT_ID}/service/trainer:${VERSION} \
    --region ${REGION} \
    --config config.yaml \
    -- \
    --data-path=train/${VERSION}/train.csv.gz \
    --eval-path=train/${VERSION}/eval.csv.gz \
    --config-path=${VERSION}/${PARAMS}.yaml \
    --model-dir=${VERSION}/${platform}/${PARAMS}/$(TZ=":UTC" date +%Y/%m/%d/%H) \
    --webhook-url=${WEBHOOK_URL}
done