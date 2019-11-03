FROM python:3.7.4-slim-stretch AS base

LABEL maintainer="Dmitry Kisler" \
  email=admin@dkisler.com \
  web=www.dkisler.com

# Required to access GCP services from ML Engine
# Installs google cloud sdk, this is mostly for using gsutil to export model.
RUN apt-get update -y \
  && apt-get install wget -y \
  && wget -nv \
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

# model version
ARG MODEL_VERSION
ENV MODEL_VERSION=${MODEL_VERSION}

# GCP buckets
ARG BUCKET_DATA
ENV BUCKET_DATA=${BUCKET_DATA}

ARG BUCKET_CONFIG
ENV BUCKET_CONFIG=${BUCKET_CONFIG}

ARG BUCKET_MODEL
ENV BUCKET_MODEL=${BUCKET_MODEL}

WORKDIR /app

# copy the service
# to be modified to "COPY . ." if using ci/cd 
# with the prior step of copying common_pkg to the service dir
COPY service/train_mleng .
COPY package libs

RUN pip install --upgrade pip \
  # install custom packages and dependencies
  && pip install --no-cache-dir pytest -r requirements.txt \
  # install model package OS dependencies
  && apt-get install libgomp1 -y \
  # && chmod +x libs/model_pkg/conversion_rate_model/${MODEL_VERSION}/os_dependencies.sh \
  # && exec libs/model_pkg/conversion_rate_model/${MODEL_VERSION}/os_dependencies.sh \
  # test the model modules
  && pytest -v libs/model_pkg/tests/*.py \
  && if [ -d libs/model_pkg/tests/${MODEL_VERSION} ]; then pytest -v libs/model_pkg/tests/${MODEL_VERSION}/; fi

ENTRYPOINT [ "python", "runner.py" ]