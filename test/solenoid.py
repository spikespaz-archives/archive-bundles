#! /usr/bin/env python3
import RPi.GPIO as GPIO
from time import sleep


# Define constants
PULSE_INTERVAL = 2
PULSE_DURATION = 4
SOLENOID_PIN = 4


if __name__ == "__main__":  # Run if this is a top level process
    GPIO.setmode(GPIO.BCM)  # Set mode to broadcom
    GPIO.setup(SOLENOID_PIN, GPIO.OUT)  # Set pin mode to output

    while True:
        GPIO.output(SOLENOID_PIN, True)
        sleep(PULSE_DURATION)
        GPIO.output(SOLENOID_PIN, GPIO.OUT)
        sleep(PULSE_INTERVAL)
