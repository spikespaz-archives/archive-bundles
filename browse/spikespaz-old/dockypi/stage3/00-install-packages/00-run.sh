#!/bin/bash -e

sh files/get-docker.sh

apt-get update

adduser pi docker
