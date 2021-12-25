#! /usr/bin/env python3
import RPi.GPIO as GPIO
from threading import Thread
from common import fullscreen_print
from sensors import moisture_reading
from go_link import claim_device
from time import sleep


SOLENOID_PIN = 4  # GPIO pin number that the solenoid is connected to
WATER_DURATION = 10  # Number of seconds that the water valve should open for
POLL_INTERVAL = 0.01  # How long of a pause between sensor polls
MOISTURE_THRESHOLD = 50  # When the moisture falls below this the valve will open


# Parent function to close a GPIO circuit and open it after a duration
def _timed_pulse(pin, duration, state):
    GPIO.output(pin, state)
    sleep(duration)
    GPIO.output(pin, not state)


# Wrapper function of _timed_pulse to be run asynchronously.
def timed_pulse(pin, duration, state=True):
    thread = Thread(target=_timed_pulse, args=(pin, duration, state))
    thread.daemon = True
    thread.start()


# Main loop to loop readings and act on them
def main_loop(device, endpoint):
    while True:
        reading = moisture_reading(device, endpoint)
        fullscreen_print(str(reading) + "%", "doh")

        if reading < MOISTURE_THRESHOLD:
            timed_pulse(SOLENOID_PIN, WATER_DURATION)

        sleep(POLL_INTERVAL)


# Run the main code if this isn't a library import
if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)  # Set pins to broadcom mode
    GPIO.setup(SOLENOID_PIN, GPIO.OUT)  # The SOLENOID_PIN as output

    try:
        main_loop(*claim_device())
    except (EOFError, KeyboardInterrupt):
        print("\nApplication closed. GPIO cleanup.")

    GPIO.cleanup()
