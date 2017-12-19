#! /usr/bin/env python3
import RPi.GPIO as GPIO
from time import sleep
from threading import Thread
from go_link import claim_device
from common import fullscreen_print
from sensors import moisture_reading

SOLENOID = 4
DURATION = 10
THRESHOLD = 50
reading = 0


def read_loop(device, endpoint):
    global reading

    while True:
        reading = moisture_reading(device, endpoint)
        # fullscreen_print(str(reading))
        print(reading)


def main_loop():
    global reading

    while True:
        if reading < THRESHOLD:
            GPIO.output(SOLENOID, False)
            print(False)
            sleep(DURATION)

        GPIO.output(SOLENOID, True)
        print(True)
        sleep(0.01)


if __name__ == "__main__":
    device, endpoint = claim_device()

    thread = Thread(target=read_loop, args=(device, endpoint))
    thread.daemon = True
    thread.start()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SOLENOID, GPIO.OUT)

    try:
        main_loop()
    except (EOFError, KeyboardInterrupt):
        print("Application closed.")

    GPIO.cleanup()
