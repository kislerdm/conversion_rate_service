FROM python:3.7.4-slim-stretch AS base

LABEL maintainer="Dmitry Kisler" \
  email=admin@dkisler.com \
  web=www.dkisler.com

VOLUME /data /model

# model version
ARG MODEL_VERSION
ENV MODEL_VERSION "v1"
# alerts webhook url
ENV WEBHOOK_URL null
# prefix to store the model
ENV PREFIX_MODEL null
# path to train and eval data sets
ENV PATH_DATA_TRAIN null
ENV PATH_DATA_EVAL null

WORKDIR /app

# copy the service
# to be modified to "COPY . ." if using ci/cd 
# with the prior step of copying common_pkg to the service dir
COPY service/train .
COPY package libs

RUN pip install --upgrade pip \
  # install custom packages and dependencies
  && pip install --no-cache-dir pytest -r requirements.txt \
  # install dependencies
  && export PATH_MISC=libs/model_pkg/conversion_rate_model/${MODEL_VERSION}/install_dependencies.sh \
  && if [ -f ${PATH_MISC} ]; then sh ${PATH_MISC}; fi \
  # test the model modules
  && pytest -v -W ignore libs/model_pkg/tests/*.py \
  && if [ -d libs/model_pkg/tests/${MODEL_VERSION} ]; then pytest -v -W ignore libs/model_pkg/tests/${MODEL_VERSION}/; fi

ENTRYPOINT [ "python", "runner.py" ]