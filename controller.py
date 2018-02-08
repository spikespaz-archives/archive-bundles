#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from json import loads
from multiprocessing import Pool
from utilities import glob_from
from subprocess import Popen, PIPE, check_output, DEVNULL
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


def get_metadata(file_path, *args, **kwargs):
    """Use FFPROBE to get information about a media file."""
    kwargs["show_format"] = kwargs.get("show_format", True)

    args = list(args)

    for arg, val in kwargs.items():
        if isinstance(val, bool):
            if val:
                args.append("-" + arg)
        else:
            args.extend(("-" + arg, val))

    return loads(check_output(("ffprobe", *args, "-of", "json", file_path), shell=True, stderr=DEVNULL))
