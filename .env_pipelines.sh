#! /bin/bash

# Dmitry Kisler © 2019
# admin@dkisler.com

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
export MODEL_PREFIX=${PREFIX}/${MODEL_VER} 
# bucket with the data set for training
export BUCKET_DATA_TRAIN=${BASE_DIR}/bucket/data/train
# path to the train data set object
export PATH_TRAIN=${PREFIX}/train.csv.gz
# path to the eval data set object
export PATH_EVAL=${PREFIX}/eval.csv.gz
## serve service
# path to the model object(s)/file(s)
export PATH_MODEL=${PREFIX}/${MODEL_VER}/model.pkl
# bucket to the data set for prediction
export BUCKET_DATA_PREDICT=${BASE_DIR}/bucket/data/predict
# path to the intup data set for prediction
export PATH_DATA_IN=input/${PREFIX}/prediction_input.csv.gz
# path to the prediction result(s)
export PATH_DATA_OUT=output/${PREFIX}/${MODEL_VER}/prediction_output.csv.gz