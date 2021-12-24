#! /usr/bin/env python3
from subprocess import Popen, DEVNULL, PIPE


class FFmpeg:
    def __init__(self, *args, stderr=DEVNULL, callback=None):
        self.args = args
        self.stderr = stderr
        self.callback = callback

    def run_async(self):
        with Popen(["ffmpeg", "-progress", "-", *self.args],
                   shell=True, stderr=self.stderr, stdout=PIPE) as ffmpeg:
            progress = {}

            while True:
                line = ffmpeg.stdout.readline().decode().split("=")

                if ffmpeg.poll() is not None:
                    break

                key = line[0].strip()

                if key == "progress":
                    if self.callback:
                        self.callback(progress)

                    yield progress

                if len(line) == 2:
                    progress[key] = line[1].strip()

    def run(self):
        return list(self.run_async())
