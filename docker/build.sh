#!/bin/bash

docker build \
    --no-cache \
    -t hardchat:latest \
    --build-arg branch=$1 \
    .
