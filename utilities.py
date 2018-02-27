#! /usr/bin/env python3

from time import clock
from os import getcwd, chdir


class WithDir:
    def __init__(self, work_dir):
        self.work_dir = work_dir

    def __enter__(self):
        self.real_dir = getcwd()
        chdir(self.work_dir)
        return self.work_dir

    def __exit__(self, *_):
        chdir(self.real_dir)
        del self.real_dir


class Reporter:
    time_start = clock()

    def report_int(self, block, block_size, total_size, precision=2):
        precision = 1024 ** precision

        current_size = block * block_size
        download_speed = current_size / (clock() - self.time_start) / precision

        total_size = total_size / precision
        current_size = current_size / precision
        percent = 100 * current_size / total_size

        return int(percent), int(current_size), int(total_size), round(download_speed, 2)

    def report_str(self, *args):
        percent, current_size, total_size, download_speed = self.report_int(*args)

        return "{:>{}}/{}mb | {:>3}% | ~{:0<4}mb/s".format(current_size, len(str(total_size)),
                                                           total_size, percent, download_speed)

    def __call__(self, *args):
        print(self.report_str(*args), end="\r")


class ChainedContext:
    def __init__(self, *managers):
        self.managers = managers

    def __enter__(self):
        self.contexts = []
        self.entrances = []

        for manager in self.managers:
            context = manager(self.entrances[-1]) if self.entrances else manager()
            self.contexts.append(context)
            self.entrances.append(context.__enter__())

        return self.entrances[-1]

    def __exit__(self, *_):
        for context in self.contexts:
            context.__exit__()
