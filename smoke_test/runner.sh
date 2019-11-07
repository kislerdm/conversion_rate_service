#! /bin/bash

# smoke test runner
# Dmitry Kisler © 2019
# admin@dkisler.com

SCRIPT_BASE_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
source ${SCRIPT_BASE_PATH}/.env.sh

msg () {
    echo "$(date +"%Y-%m-%d %H:%M:%S") $1"
}

msg "Start end2end smoke test"

msg "Test: check required buckets/dirs"
prefix=${BASE_DIR}/bucket
dirs=(data/train data/predict data/predict/input data/predict/output model)
for d in ${dirs[@]}; do
  if [ ! -d ${prefix}/${d} ]; then
    msg "Error: bucket/dir ${prefix}/${d} doesn't exist"
    msg "smoke test [FAILED]"
    exit 1
  fi
done
msg "[PASSED]"

msg "Test: trigger train service"
if [ ! -d ${BUCKET_DATA_TRAIN}/${PREFIX} ]; then 
  mkdir -p ${BUCKET_DATA_TRAIN}/${PREFIX}
fi
cp -r ${SCRIPT_BASE_PATH}/data/train/*.csv.gz ${BUCKET_DATA_TRAIN}/${PREFIX}
docker-compose -f ${BASE_DIR}/app/compose-train.yaml up
flag=$?
rm -rf ${BUCKET_DATA_TRAIN}/${PREFIX}
if [ ! ${flag} -eq 0 ]; then
  msg "Train service test [FAILED]"
  exit 1
fi

if [ ! -f ${BUCKET_MODEL}/${PATH_MODEL} ]; then
  msg "Train service test [FAILED]"
  exit 1
fi
msg "[PASSED]"

msg "Test: trigger serve service"
if [ ! -d ${BUCKET_DATA_PREDICT}/input/${PREFIX} ]; then 
  mkdir -p ${BUCKET_DATA_PREDICT}/input/${PREFIX}
fi
cp -r ${SCRIPT_BASE_PATH}/data/predict/prediction_input.csv.gz ${BUCKET_DATA_PREDICT}/input/${PREFIX}
if [ ! -f ${BUCKET_MODEL}/${PATH_MODEL} ]; then
  cp -r ${SCRIPT_BASE_PATH}/model/${MODEL_VER}/* ${BUCKET_MODEL}/${MODEL_PREFIX}
fi
docker-compose -f ${BASE_DIR}/app/compose-serve.yaml up
flag=$?
if [ ! ${flag} -eq 0 ]; then
  rm -rf ${BUCKET_MODEL}/${MODEL_PREFIX} ${BUCKET_DATA_PREDICT}/input/${PREFIX}
  msg "Serve service test [FAILED]"
  exit 1
fi

# test prediction output complience with SLA
header=$(zless ${BUCKET_DATA_PREDICT}/${PATH_DATA_OUT} | head -1)
if [ ${header} != "${SLA_HEADER}" ]; then
  rm -rf ${BUCKET_MODEL}/${MODEL_PREFIX} \
         ${BUCKET_DATA_PREDICT}/input/${PREFIX} \
         ${BUCKET_DATA_PREDICT}/output/${PREFIX}
  msg "Serve service test [FAILED]"
  msg "Output data don't match output SLA"
  exit 1
fi

vals=$(zless ${BUCKET_DATA_PREDICT}/${PATH_DATA_OUT} | tail -1 | awk -F "." '{print $1}')
if [ ${vals} != "${EXPECTED_OUTPUT}" ]; then
  msg "WARNING! Prediction results don't match expectations. Check the model definition."
fi

msg "[PASSED]"

rm -rf ${BUCKET_MODEL}/${PREFIX} \
       ${BUCKET_DATA_PREDICT}/input/${PREFIX} \
       ${BUCKET_DATA_PREDICT}/output/${PREFIX}
msg "end2end smoke test [PASSED]"