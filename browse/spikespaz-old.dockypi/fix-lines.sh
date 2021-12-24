#!/bin/bash -e

find . -type f -iname "*.sh" -print0 | xargs -0 dos2unix
