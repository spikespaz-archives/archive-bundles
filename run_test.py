#! /usr/bin/env python3
from sys import argv
from time import sleep


def test_fullscreen_print():
    from time import sleep
    from lib_common import fullscreen_print

    counter = 100

    while counter > 0:
        fullscreen_print(str(counter))
        counter -= 1
        sleep(0.01)


def test_log_line():
    from lib_common import log_line

    def write_test(log_file):
        log_line(log_file, "Started log test.")

        for line in range(5):
            log_line(log_file, "Test line " + str(line))

        for line in range(5):
            log_line(log_file, "Test warn line " + str(line), level="warn")

        for line in range(5):
            log_line(log_file, "Test indented line " + str(line), indent=4)

        for line in range(5):
            log_line(log_file, "Test indented warn line " + str(line), level="warn", indent=4)

        log_line(log_file, "Finished log test.")

    with open("logs/test_a.txt", "a") as log_file:
        write_test(log_file)

    with open("logs/test_aplus.txt", "a+") as log_file:
        write_test(log_file)

    with open("logs/test_wplus.txt", "w+") as log_file:
        write_test(log_file)


def test_solenoid_pin():
    import RPi.GPIO as GPIO
    from time import sleep

    PULSE_INTERVAL = 2
    PULSE_DURATION = 4
    SOLENOID_PIN = 4

    GPIO.setmode(GPIO.BCM)  # Set mode to broadcom
    GPIO.setup(SOLENOID_PIN, GPIO.OUT)  # Set pin mode to output

    while True:
        GPIO.output(SOLENOID_PIN, True)
        sleep(PULSE_DURATION)
        GPIO.output(SOLENOID_PIN, GPIO.OUT)
        sleep(PULSE_INTERVAL)


test_map = {
    "figlet": test_fullscreen_print,
    "logger": test_log_line,
    "solenoid": test_solenoid_pin
}


if len(argv) > 1:
    exceptions = []
    print("Starting", len(argv) - 1, "test" + ("s." if len(argv) - 1 > 1 else "."))

    for test in argv[1:]:
        if test in test_map:
            try:
                print("Starting test:", test)
                sleep(2)
                test_map[test]()
            except Exception as error:
                exceptions.append(error)
                print("Failed with exception:", error)
        else:
            print("Test not found:", test)

    print("Completed tests:", ", ".join(argv[1:]), "\n", len(exceptions), "failed.")

    if exceptions:
        print("\nExceptions:\n", "\n".join(map(lambda x: str(x), exceptions)))
