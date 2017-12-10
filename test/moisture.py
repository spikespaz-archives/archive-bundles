#! /usr/bin/env python3
from ..vernierlib import claim_device, moisture_reading
from time import sleep

device, endpoint = claim_device()

while True:
    print(moisture_reading(device, endpoint))
    sleep(1)
