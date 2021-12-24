#! /usr/bin/env python3
from common import log_line


def write_test(log_file):
    log_line(log_file, "Starting Log.")

    for num in range(20):
        log_line(log_file, "Counted to: " + str(num))

    for num in range(20):
        log_line(log_file, "Counted to: " + str(num), indent=4)

    for num in range(20):
        log_line(log_file, "Counted to: " + str(num), indent=8)

    for num in range(20):
        log_line(log_file, "Counted to: " + str(num), level="warn")

    for num in range(20):
        log_line(log_file, "Counted to: " + str(num), level="info")


with open("logs/test_a.txt", "a") as test_file:
    write_test(test_file)

with open("logs/test_ap.txt", "a+") as test_file:
    write_test(test_file)

with open("logs/test_wp.txt", "w+") as test_file:
    write_test(test_file)
