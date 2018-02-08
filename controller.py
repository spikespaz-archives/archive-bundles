#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from json import loads
from subprocess import Popen, check_output, DEVNULL, PIPE


def run_ffmpeg(input_file, output_file, async=True, *args, **kwargs):
    """Use FFMPEG to convert a media file."""
    kwargs["y"] = kwargs.get("y", True)

    args = list(args)

    for arg, val in kwargs.items():
        if isinstance(val, bool):
            if val:
                args.append("-" + arg)
        else:
            args.extend(("-" + arg, val))

    ffmpeg = Popen(("ffmpeg", *args, "-progress", "-", "-i", input_file, output_file),
                   shell=True, stderr=DEVNULL, stdout=PIPE)

    if not async:
        return ffmpeg.wait()
    else:
        data = {}

        while True:
            line = ffmpeg.stdout.readline().decode().split("=")

            if ffmpeg.poll() is not None:
                break

            key = line[0].strip()

            if key == "progress":
                yield data

            if len(line) == 2:
                data[key] = line[1].strip()


def run_ffprobe(file_path, *args, **kwargs):
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
