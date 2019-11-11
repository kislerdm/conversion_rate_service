#! /bin/bash

DATA_VER=features_v1
PREFIX=$(date +'%Y/%m/%d')/e2e_test

export BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." >/dev/null && pwd )"

SLA_HEADER="entity_id,device,cr"
EXPECTED_OUTPUT="6,Computer,0"

export MODEL_VER="v1"
export BUCKET_MODEL=${BASE_DIR}/bucket/model
# train service
export MODEL_PREFIX=${MODEL_VER}/${PREFIX}
export BUCKET_DATA_TRAIN=${BASE_DIR}/bucket/data/train/${DATA_VER}
export PATH_TRAIN=${PREFIX}/train.csv.gz
export PATH_EVAL=${PREFIX}/eval.csv.gz
# serve service
export PATH_MODEL=${MODEL_VER}/${PREFIX}/model.pkl
export BUCKET_DATA_PREDICT=${BASE_DIR}/bucket/data/predict
export PATH_DATA_IN=input/${DATA_VER}/${PREFIX}/prediction_input.csv.gz
export PATH_DATA_OUT=output/${DATA_VER}/${PREFIX}/prediction_output.csv.gz