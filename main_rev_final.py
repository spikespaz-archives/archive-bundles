#! /usr/bin/env python3
import usb.util
import RPi.GPIO as GPIO
from threading import Thread
from lib_golink import claim_device, find_device
from lib_common import fullscreen_print, log_line
from lib_sensors import moisture_reading
from time import sleep, strftime


SOLENOID_PIN = 4  # GPIO pin number that the solenoid is connected to
WATER_DURATION = 30  # Number of seconds that the water valve should open for
POLL_INTERVAL = 5  # How long of a pause between sensor polls
MOISTURE_THRESHOLD = 50  # When the moisture falls below this the valve will open


# Parent function to close a GPIO circuit and open it after a duration
def _timed_pulse(pin, duration, state, log_file=None):
    GPIO.output(pin, state)  # Set the output of the pin to the state (default high)
    log_line(log_file, "Set pin " + str(pin) + " to " +
             ("high" if state else "low") + " signal. Waiting " + str(duration) + " seconds.")
    sleep(duration)  # Wait a specified time in seconds
    GPIO.output(pin, not state)  # Set the output of the pin to the opposite of the state (low)
    log_line(log_file, "Set pin " + str(pin) + " to " + ("low" if state else "high") + ".")


# Wrapper function of _timed_pulse to be run asynchronously.
def timed_pulse(pin, duration, state=True, log_file=None):
    thread = Thread(target=_timed_pulse, args=(pin, duration, state, log_file))  # Create the thread with
    # the target pointing to the parent function, and give it args
    thread.daemon = True  # Let the program die before this is finished
    thread.start()  # Start the worker thread


# Main loop to loop readings and act on them
def main_loop(device, endpoint, log_file):
    while True:  # Infinite loop, run forever
        reading = moisture_reading(device, endpoint)  # Save the reading from the sensor to a variable

        if reading is None:
            log_line(log_file, "Failed sensor reading. Make sure enough power is supplied.", indent=2)
            continue

        fullscreen_print(str(reading) + "%", "doh", top_pad=3)  # Pretty print that to the terminal.
        log_line(log_file, "Moisture Level: " + str(reading) + "%", indent=2)

        if reading < MOISTURE_THRESHOLD:  # If the reading above is below the allowed moisture level
            log_line(log_file, "Triggered timed pulse at moisture level: " + str(reading) + "%")
            timed_pulse(SOLENOID_PIN, WATER_DURATION, log_file=log_file)  # Pulse the pin for a duration

        sleep(POLL_INTERVAL)  # Wait some time before continuing the loop


# Run the main code if this isn't a library import
if __name__ == "__main__":
    log_file = open(strftime("logs/%a-%m-%d-%Y.%I-%M%p.txt"), "a")
    log_line(log_file, "Starting current log file.")
    log_line(log_file, "SOLENOID_PIN = " + str(SOLENOID_PIN))
    log_line(log_file, "WATER_DURATION = " + str(SOLENOID_PIN))
    log_line(log_file, "POLL_INTERVAL = " + str(SOLENOID_PIN))
    log_line(log_file, "MOISTURE_THRESHOLD = " + str(SOLENOID_PIN))

    GPIO.setmode(GPIO.BCM)  # Set pins to broadcom mode

    log_line(log_file, "Set GPIO pins to broadcom mode.")
    GPIO.setup(SOLENOID_PIN, GPIO.OUT)  # The SOLENOID_PIN as output
    log_line(log_file, "Set GPIO pin " + str(SOLENOID_PIN) + " to output.")

    try:
        log_line(log_file, "Automatically searching for a device to claim.")
        device, endpoint = claim_device()  # Attempt to auto-claim the device endpoint
    except ConnectionError:  # claim_device raises ConnectionError when a device isn't found, so catch that
        log_line(log_file, "No device automatically found. Reverting to manual connection.")
        device, endpoint = claim_device(find_device())  # Try again, maybe the device is unplugged?

    log_line(log_file, "Device found: " + usb.util.get_string(device, device.iProduct) +
                       " by " + usb.util.get_string(device, device.iManufacturer))

    try:
        log_line(log_file, "Device connected successfully, beginning main loop.")
        main_loop(device, endpoint, log_file)  # Start the main loop with device, endpoint expanded from connection
    except (EOFError, KeyboardInterrupt):  # The user naturally and manually canceled the process
        print("\nApplication closed. GPIO cleanup.")  # Tell the user that the program listened
        log_line(log_file, "EOFError or KeyboardInterrupt received, exiting application.")

    GPIO.cleanup()  # Clean up all GPIO connections and reset states

    log_line(log_file, "Cleaned up GPIO connections. Exiting now.")
