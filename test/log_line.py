#! /usr/bin/env python3
from ..lib_common import log_line


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
