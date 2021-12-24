#! /usr/bin/env python3
from ..lib_common import fullscreen_print
from time import sleep


counter = 100

while True:
    fullscreen_print(str(counter))
    counter -= 1
    sleep(2)
