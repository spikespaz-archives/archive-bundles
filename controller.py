#! /usr/bin/env python3

from subprocess import Popen, PIPE


def convert_file_function(input_path, output_path, overwrite=False):
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

                time = record  # Extract the data
            else:
                continue  # No match found yet for buffer, continue

            buffer, record = "", ""  # Reset both buffers
            yield time, speed  # Return a tuple of the extracted data of time (h, m, s, ms) and speed
