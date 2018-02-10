#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from glob import glob
from json import loads
from inspect import stack
from multiprocessing import Pool, Lock
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


def run_ffmpeg(input_file, output_file, async=False, *args, **kwargs):
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


def run_ffmpeg_async(*args, **kwargs):
    """Run FFMPEG and yield updates. Alias for `run_ffmpeg(*args, **kwargs, async=True)`."""
    yield from run_ffmpeg(*args, **kwargs, async=True)


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
    """Wrapper around `run_ffprobe` and `run_ffmpeg` that can perform a batch conversion
    on files and output to a mirror directory."""

    def __init__(self, input_dir, output_dir, input_fmt="flac", output_fmt="mp3", workers=4, callbacks={}):
        """Initialize the wrapper with all input and output parameters specified. Provide optional callbacks."""
        self.input_dir = input_dir
        self.output_dir = output_dir

        self.input_fmt = input_fmt
        self.output_fmt = output_fmt

        self.workers = workers

        self._callbacks = self._wrap_callbacks(**callbacks)

        self.file_paths = glob(os.path.join(input_dir, "**/*." + input_fmt.lower()))

        self._unfinished = []
        self.batch_meta = []
        self.last_pool = None
        self.mutex = Lock()

    def _callback(self, result, callback=stack()[1][3]):
        """Wrapper to retrieve a callback matching the parent method name from `self.callbacks` if it exists.
        This is very metaprogrammed and bad practice. May be removed."""
        callback = self._callbacks.get(callback)

        if callback is not None:
            callback(result)

    def _task_queue(self):
        """Get the protected task queue from within the `self.last_pool`. Will error if `self.last_pool` is None."""
        return self.last_pool._taskqueue

    def _batch_ffprobe_callback(self, result):
        """Callback wrapper for a list of `run_ffprobe` results that sets the internal `self.batch_meta`
        field and wraps the optional callback."""
        self.batch_meta = result

    def _batch_ffprobe_callback_async(self, result):
        """Callback wrapper for each asynchronous `run_ffprobe` result that adds to the internal `self.batch_meta`
        field and wraps the optional callback."""
        self.batch_meta.append(result)

    def _wrap_callbacks(self, **kwargs):
        """Initialization method to wrap callbacks with required code."""
        def _run_batch_ffprobe(result):
            callback = kwargs.get(stack()[0][3][1:])

            with self.mutex:
                self.batch_meta = result

            if callback:
                callback(result)

        def _run_batch_ffprobe_async(result):
            callback = kwargs.get(stack()[0][3][1:])

            with self.mutex:
                self.batch_meta.append(result)

            if callback:
                callback(result)

        kwargs.update(
            run_batch_ffprobe=_run_batch_ffprobe,
            run_batch_ffprobe_async=_run_batch_ffprobe_async
        )

        return kwargs

    def set_callbacks(self, **kwargs):
        """Set the callbacks by keyword arguments."""
        self._callbacks = self._wrap_callbacks(**kwargs)

    def run_batch_ffprobe(self):
        """Execute `run_ffprobe` on a batch of files synchronously, update `self.batch_meta`, and return the results."""
        with Pool(self.workers) as pool:
            self.last_pool = pool

            return pool.map_async(run_ffprobe, self.file_paths, callback=self._callback)

    def run_batch_ffprobe_async(self):
        """Execute `run_ffprobe` on a batch of files asynchronously while apppending to `self.batch_meta` and return
        the worker pool before all results are ready."""
        self.last_pool = Pool(self.workers)

        for file_path in self.file_paths:
            self.last_pool.apply_async(run_ffprobe, (file_path,), callback=self._callback)

        return self.last_pool

    def run_batch_ffmpeg(self):
        """Execute `run_ffmpeg` on a batch of files synchronously and return the results."""
        with Pool(self.workers) as pool:
            self.last_pool = pool

            return pool.map_async(run_ffmpeg, self.file_paths, callback=self._callback)

    def run_batch_ffmpeg_async(self):
        """Execute `run_ffmpeg` on a batch of files asynchronously and return
        the worker pool before all results are ready."""
        self.last_pool = Pool(self.workers)

        for file_path in self.file_paths:
            self.last_pool.apply_async(run_ffmpeg, (file_path,), callback=self._callback)

        return self.last_pool

    def run_batch_ffmpeg_gen(self):
        """Execute `run_ffmpeg_async` on a batch of files synchronously and return the results.
        Callback must be able to handle a generator."""
        with Pool(self.workers) as pool:
            self.last_pool = pool

            return pool.map_async(run_ffmpeg_async, self.file_paths, callback=self._callback)

    def run_batch_ffmpeg_gen_async(self):
        """Execute `run_ffmpeg_async` on a batch of files asynchronously and return
        the worker pool before all results are ready. Callback must be able to handle a generator."""
        self.last_pool = Pool(self.workers)

        for file_path in self.file_paths:
            self.last_pool.apply_async(run_ffmpeg_async, (file_path,), callback=self._callback)

        return self.last_pool

    def start(self):
        self.run_batch_ffprobe()
        self._callback(self.last_pool)

    def start_async(self):
        self.run_batch_ffprobe_async()

        self.last_pool.close()
        self.last_pool.join()

        self._callback(self.last_pool)

    def wait(self):
        """Close and join `self.last_pool`."""
        self.last_pool.close()
        self.last_pool.join()

    def pause(self):
        """Pause the batch operation in `self.last_pool` by adding all incomplete tasks to a protected internal field
        and empty the protected queue. Run the callback matching the name of this method. Non blocking."""
        if self.last_pool and not self._unfinished:
            queue = self._task_queue()

            with queue.mutex:
                while len(queue.queue) <= 0:
                    self._unfinished.append(queue.get())

            self._callback(self.last_pool)

    def resume(self):
        """Move all internally saved incomplete processes back into the protected queue,
        and restart and maintain workers if needed. Run the callback matching the name of this method."""
        if self.last_pool and self._unfinished:
            for task in self._unfinished:
                self.last_pool.put(task)

            self._unfinished = []

            self.last_pool._maintain_pool()

            self._callback(self.last_pool)

    def cancel(self):
        """Completely lock, clear, and close the internal protected queue of `self.last_queue` while allowing current
        workers to finish while blocking. Run the callback matching the name of this method."""
        if self.last_pool:
            queue = self._task_queue()

            with queue.mutex:
                queue.queue.clear()
                self.last_pool.close()

            self.last_pool.join()

            self._callback(self.last_pool)

    def terminate(self):
        """Terminate all workers and clear the internal incomplete list if paused."""
        if self.last_pool:
            self.last_pool.terminate()
            self._unfinished = []

            self._callback(self.last_pool)

    def get_finished(self):
        """The count of finished conversion processes."""
        return len(self.batch_meta)

    def get_unfinished(self):
        """The count of unfinished conversion processes."""
        return len(self.file_paths) - self.get_finished()
