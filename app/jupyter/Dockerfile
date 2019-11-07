FROM python:3.7.4-slim-stretch AS base

LABEL maintainer="Dmitry Kisler" \
  email=admin@dkisler.com \
  web=www.dkisler.com

VOLUME /transfer

COPY jupyter .

RUN apt-get update -y \
  && apt-get install libgomp1 -y \
  && pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt \
  && useradd -ms /bin/bash jupyter \
  && chmod -R 664 /transfer

USER jupyter

ENV PORT 8888
EXPOSE ${PORT}

ENTRYPOINT jupyter-lab /transfer \
    --no-browser \
    --NotebookApp.token='' \
    --NotebookApp.password='' \
    --log-level=ERROR \
    --ip=0.0.0.0 \
    --port=${PORT}
