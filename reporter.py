#! /usr/bin/env python3

from time import clock


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

        return "{:>{}}/{}mb - {:>3}% - ~{:0<4}mb/s".format(current_size, len(str(total_size)),
                                                           total_size, percent, download_speed)

    def __call__(self, *args):
        print(self.report_str(*args), end="\r")
