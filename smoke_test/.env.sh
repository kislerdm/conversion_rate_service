#! /bin/bash

PREFIX=$(date +'%Y/%m/%d')/e2e_test

export BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." >/dev/null && pwd )"

SLA_HEADER="entity_id,platform,cr"
EXPECTED_OUTPUT="20458,1,0"

export MODEL_VER="v1"
export BUCKET_MODEL=${BASE_DIR}/bucket/model
# train service
export MODEL_PREFIX=${PREFIX}/${MODEL_VER} 
export BUCKET_DATA_TRAIN=${BASE_DIR}/bucket/data/train
export PATH_TRAIN=${PREFIX}/train.csv.gz
export PATH_EVAL=${PREFIX}/eval.csv.gz
# serve service
export PATH_MODEL=${PREFIX}/${MODEL_VER}/model.pkl
export BUCKET_DATA_PREDICT=${BASE_DIR}/bucket/data/predict
export PATH_DATA_IN=input/${PREFIX}/prediction_input.csv.gz
export PATH_DATA_OUT=output/${PREFIX}/prediction_output.csv.gz