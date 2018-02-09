#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from utilities import glob_from
from glob import glob
from json import loads
from multiprocessing import Pool
from multiprocessing.queues import Empty
from subprocess import Popen, check_output, DEVNULL, PIPE


def arg_builder(args, kwargs, defaults={}):
    """Build arguments from `args` and `kwargs` in a shell-lexical manner."""
    for key, val in defaults.items():
        kwargs[key] = kwargs.get(key, val)

    args = list(args)

    for arg, val in kwargs.items():
        if isinstance(val, bool):
            if val:
                args.append("-" + arg)
        else:
            args.extend(("-" + arg, val))

    return args


def run_ffmpeg(input_file, output_file, async=True, *args, **kwargs):
    """Use FFMPEG to convert a media file."""
    with Popen(("ffmpeg", *arg_builder(args, kwargs, defaults={"y": True}),
                "-progress", "-", "-i", input_file, output_file),
               shell=True, stderr=DEVNULL, stdout=PIPE) as ffmpeg:
        if async:
            progress = {}

            while True:
                line = ffmpeg.stdout.readline().decode().split("=")

                if ffmpeg.poll() is not None:
                    break

                key = line[0].strip()

                if key == "progress":
                    yield progress

                if len(line) == 2:
                    progress[key] = line[1].strip()

        else:
            return ffmpeg.wait()


def run_ffprobe(file_path, *args, **kwargs):
    """Use FFPROBE to get information about a media file."""
    return loads(check_output(("ffprobe", *arg_builder(args, kwargs, defaults={"show_format": True}),
                               "-of", "json", file_path), shell=True, stderr=DEVNULL))


def batch_ffprobe(file_paths, workers=4):
    with Pool(workers) as pool:
        return pool.map(run_ffprobe, file_paths)


def batch_ffprobe_async(file_paths, workers=4, callback=None):
    pool = Pool(workers)

    for file_path in file_paths:
        pool.apply_async(run_ffprobe, (file_path,), callback=callback)

    return pool


class BatchMediaConverter:
    def __init__(self, input_dir, output_dir, input_fmt="flac", output_fmt="mp3", workers=4, callbacks={}):
        self.input_dir = input_dir
        self.output_dir = output_dir

        self.input_fmt = input_fmt
        self.output_fmt = output_fmt

        self.workers = workers

        self.callbacks = callbacks

        self.batch_meta = []
        self.last_pool = None

        self.file_paths = glob(os.path.join(input_dir, "**/*." + input_fmt.lower()))

    def retrieve_batch_meta(self):
        with Pool(self.workers) as pool:
            self.last_pool = pool

            return pool.map_async(run_ffprobe, self.file_paths, callback=self.callbacks.get("batch_meta"))

    def retrieve_batch_meta_async(self):
        self.last_pool = Pool(self.workers)

        for file_path in self.file_paths:
            self.last_pool.apply_async(run_ffprobe, (file_path,), callback=self.callbacks.get("batch_meta_async"))

        return self.last_pool

    def start(self):
        self.retrieve_batch_meta()

    def start_async(self):
        self.retrieve_batch_meta_async()

    def cancel(self):
        if self.last_pool:
            queue = self.last_pool._taskqueue

            with queue.mutex:
                unfinished = queue.unfinished_tasks

                if unfinished <= 0:
                    if unfinished < 0:
                        raise ValueError('task_done() called too many times')
                    queue.all_tasks_done.notify_all()

                queue.queue.clear()
                queue.unfinished_tasks = unfinished

                self.last_pool.close()

        callback = self.callbacks.get("cancel")

        if callback:
            callback(self.last_pool)

    def terminate(self):
        if self.last_pool:
            self.last_pool.terminate()

            callback = self.callbacks.get("terminate")

            if callback:
                callback(self.last_pool)
