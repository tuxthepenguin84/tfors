# syntax=docker/dockerfile:1
# docker build -f Dockerfile . -t tuxthepenguin/tfors:latest --no-cache
FROM ubuntu:focal
ENV TFORSMODELURL=https://tfhub.dev/tensorflow/centernet/resnet50v1_fpn_512x512/1
ENV TFORSENCODING=utf-8
ENV TFORSBUFFER=4096
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python-is-python3 \
    build-essential \
    python3-dev \
    git \
    protobuf-compiler \
    apt-transport-https \
    ca-certificates \
 && update-ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && git clone https://github.com/tuxthepenguin84/tfors.git tfors \
 && git clone --depth 1 https://github.com/tensorflow/models \
 && cd models/research/ \
 && protoc object_detection/protos/*.proto --python_out=. \
 && cp object_detection/packages/tf2/setup.py . \
 && python -m pip install . \
 && pip install httplib2
HEALTHCHECK CMD curl -f http://localhost:4949 || exit 1
EXPOSE 4949/tcp
CMD python -u /tfors/server.py -d -l /models/research/object_detection/data/mscoco_label_map.pbtxt -m $TFORSMODELURL -b $TFORSBUFFER  -e $TFORSENCODING