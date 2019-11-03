FROM python:3.7.4-slim-stretch AS base

LABEL maintainer="Dmitry Kisler" \
  email=admin@dkisler.com \
  web=www.dkisler.com

# Required to access GCP services from ML Engine
# Installs google cloud sdk, this is mostly for using gsutil to export model.
RUN wget -nv \
  https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz \
  && mkdir /root/tools \
  && tar xvzf google-cloud-sdk.tar.gz -C /root/tools \
  && rm google-cloud-sdk.tar.gz  \
  && /root/tools/google-cloud-sdk/install.sh --usage-reporting=false \
    --path-update=false --bash-completion=false \
    --disable-installation-options \
  && rm -rf /root/.config/* \
  && ln -s /root/.config /config \
  && rm -rf /root/tools/google-cloud-sdk/.install/.backup

# Path configuration
ENV PATH $PATH:/root/tools/google-cloud-sdk/bin
# Make sure gsutil will use the default service account
RUN echo '[GoogleCompute]\nservice_account = default' > /etc/boto.cfg

VOLUME /data /model /config

ARG WEBHOOK_URL=null
# model version
ARG MODEL_VERSION
# GCP buckets
ARG BUCKET_DATA
ARG BUCKET_CONFIG
ARG BUCKET_MODEL

WORKDIR /app

# copy the service
# to be modified to "COPY . ." if using ci/cd 
# with the prior step of copying common_pkg to the service dir
COPY service/train_mleng .
COPY package libs

RUN pip install --upgrade pip \
  # install custom packages and dependencies
  && pip install --no-cache-dir pytest -r requirements.txt \
  # test the model modules
  && pytest -v libs/model_pkg/tests/*.py \
  && if [ -d libs/model_pkg/tests/${MODEL_VERSION} ]; then pytest -v libs/model_pkg/tests/${MODEL_VERSION}/; fi

ENTRYPOINT [ "python", "runner.py" ]