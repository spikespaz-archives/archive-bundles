#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from multiprocessing import Pool
from utilities import glob_from
from subprocess import Popen, PIPE
from re import findall, MULTILINE


def async_convert_file(input_path, output_path, overwrite=False):
    """Convert a file (and maybe overwrite) with FFMPEG and yield `(time, speed)` periodically."""
    ffmpeg = Popen(("ffmpeg", "-i", input_path, output_path, "-y" if overwrite else "-n"),
                   shell=True, stderr=PIPE)

    def get_stderr():
        return ffmpeg.stderr.read(1).decode()  # Grab one character from stderr and make it unicode

    buffer = ""  # Buffer for building matching strings
    record = ""  # Buffer for storing the data following

    time, speed = "00:00:00.00", 0.0  # The variables to be extracted

    while True:  # Loop through the stderr until break
        stderr = get_stderr()  # Each character

        if stderr == "" and ffmpeg.poll() is not None:
            break  # Stream ended end the loop
        else:
            buffer += stderr  # Add the character to the buffer

            if buffer.endswith("speed="):  # Match the start of the data section
                while not record.endswith("x"):
                    record += get_stderr()  # Add one more character until it matches the loop condition

                speed = float(record[:-1])  # Extract the data
            elif buffer.endswith("time="):
                while len(record) < 11:
                    record += get_stderr()

                time = record.replace(".", ":").split(":")  # Extract the time, in seconds
                time = int(time[0]) * 216000 + int(time[1]) * 3600 + int(time[2]) * 60 + int(time[3])
            else:
                continue  # No match found yet for buffer, continue

            buffer, record = "", ""  # Reset both buffers
            yield time, speed  # Return a tuple of the extracted data of time (h, m, s, ms) and speed


def get_metadata(file_path):
    """Use FFPROBE to get information about a media file."""
    stderr = Popen(("ffprobe", file_path), shell=True, stderr=PIPE).communicate()[1].decode()

    metadata = {}

    for match in findall(r"(\w+)\s+:\s(.+)\r$", stderr, MULTILINE):
        metadata[match[0].lower()] = match[1]

    return metadata
