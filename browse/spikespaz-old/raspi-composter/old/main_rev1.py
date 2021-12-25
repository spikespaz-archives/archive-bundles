#! /usr/bin/env python3
import RPi.GPIO as GPIO
from time import sleep, time, strftime
from go_link import claim_device
from sensors import moisture_reading

# Define GPIO constants based on the table above.
motor_enable = 0  # The pin that controls the state of the active motor
motor_control = 0  # The pin that controls the rotation of the motor
solenoid = 7  # The pin that controls the state of the solenoid

valve_threshold = 50  # The moisture level at wh;ich the water flow will start

log_file_name = strftime("logs/%Y-%m-%d %H:%M:%S.log")
log_file = open(log_file_name, "a")


def open_valve(state=True):  # Set the valve open state
    GPIO.output(solenoid, not state)  # Needs to be reversed because
    # when the GPIO is high the valve is closed.


def toggle_valve():  # Reverse the current state of the valve
    GPIO.output(solenoid, GPIO.input(solenoid))  # Set the valve to the reverse of the current state


def water_loop():
    device, endpoint = claim_device()  # Get the claimed device object and endpoint
    last_opened = 0  # Sets the current last opened time

    while True:  # Run this forever
        log_file.write(strftime("  [%H:%M:%S] ") + str(moisture_reading(device, endpoint)) + "\n")
        # Log the current time and reading to a file

        if moisture_reading(device, endpoint) < valve_threshold and last_opened + 3600 < time():
            # If the moisture level is less than allowed and the last opened time was one hour ago or more
            last_opened = time()
            log_file.write(strftime("[%H:%M:%S] Open the valve.") + "\n")  # Log open
            open_valve(True)  # Open the valve

            while time() < last_opened + 30:
                log_file.write(strftime("  [%H:%M:%S] ") + str(moisture_reading(device, endpoint)) + "\n")

            sleep(30)  # Run the motor for 30s
            open_valve(False)  # Close the valve
            log_file.write(strftime("[%H:%M:%S] Closed the valve.") + "\n")  # Log closed

        sleep(5)
        print(moisture_reading(device, endpoint))


if __name__ == "__main__":
    GPIO.cleanup()  # Close all existing connections
    log_file.write(strftime("[%H:%M:%S] Started logging.") + "\n")  # Notify the log that it has started
    GPIO.setmode(GPIO.BCM)  # Set the pin mode to broadcom

    GPIO.setup(motor_enable, GPIO.OUT)  # Set the motor_enable pin as output
    GPIO.setup(motor_control, GPIO.OUT)  # Set the motor_control pin as output
    GPIO.setup(solenoid, GPIO.OUT)  # Set the solenoid pin as output

    GPIO.output(motor_enable, True)  # Always keep the motor_enable pin on, so it can rotate

    try:
        water_loop()  # Run the infinite loop that enables water flow based on moisture level
    except (KeyboardInterrupt, EOFError) as e:
        print("KeyboardInterrupt received, closing application.")
        log_file.write(strftime("[%H:%M:%S] Stopped logging.") + "\n")  # Notify the log that it has stopped

    GPIO.cleanup()  # Will never run, but nice to have here because why not
    log_file.close()   # Close the file, will also never be called
