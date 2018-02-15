#!/bin/bash -e

sh ${BASE_DIR}/scripts/get-docker.sh

apt-get update

usermod -aG docker pi
