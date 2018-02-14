#!/bin/bash -e

sh ${BASE_DIR}/get-docker.sh

apt-get update

usermod -aG docker pi
