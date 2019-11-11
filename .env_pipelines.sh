#! /bin/bash

# Dmitry Kisler © 2019
# www.dksiler.com

# features engineering version
DATA_VER=features_v1
PREFIX=$(date +'%Y/%m/%d')

export BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
# webhook URL
export WEBHOOK=null
# model version for current deployment
export MODEL_VER="v1"
# bucket with models metadata
export BUCKET_MODEL=${BASE_DIR}/bucket/model
## train service
# path to the model object(s)/"folder"
export MODEL_PREFIX=${MODEL_VER}/${PREFIX}
# bucket with the data set for training
export BUCKET_DATA_TRAIN=${BASE_DIR}/bucket/data/train/${DATA_VER}
# path to the train data set object
export PATH_TRAIN=${PREFIX}/train.csv.gz
# path to the eval data set object
export PATH_EVAL=${PREFIX}/eval.csv.gz
## serve service
# path to the model object(s)/file(s)
export PATH_MODEL=${MODEL_VER}/${PREFIX}/model.pkl
# bucket to the data set for prediction
export BUCKET_DATA_PREDICT=${BASE_DIR}/bucket/data/predict
# path to the intup data set for prediction
export PATH_DATA_IN=input/${DATA_VER}/${PREFIX}/prediction_input.csv.gz
# path to the prediction result(s)
export PATH_DATA_OUT=output/${DATA_VER}/${PREFIX}/prediction_output.csv.gz