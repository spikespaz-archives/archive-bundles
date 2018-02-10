#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import utilities as utils

from json import loads
from inspect import stack
from functools import wraps
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


def get_ow_args(overwrite=False):
    """Return a dictionary that can be passed as args to FFMPEG telling it to overwrite or not."""
    return {"y": overwrite, "n": not overwrite}


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


class BatchController:
    """Wrapper around `run_ffprobe` and `run_ffmpeg` that can perform a batch conversion
    on files and output to a mirror directory."""

    def __init__(self, input_dir, output_dir, input_fmt="flac", output_fmt="mp3", overwrite_output=False, workers=4, callbacks={}):
        """Initialize the wrapper with all input and output parameters specified. Provide optional callbacks."""
        self._input_dir = input_dir
        self._output_dir = output_dir

        self._input_fmt = input_fmt.lower()
        self._output_fmt = output_fmt.lower()

        self._overwrite_output = overwrite_output

        self._workers = workers

        self._callbacks = self._wrap_callbacks(**callbacks)

        glob_paths = utils.glob_from(input_dir, "**/*." + input_fmt)

        self._input_paths = [os.path.join(input_dir, path_name) for path_name in glob_paths]
        self._output_paths = [utils.replace_base(input_dir, output_dir, utils.replace_ext(path_name, output_fmt))
                              for path_name in glob_paths]

        self._ow_args = get_ow_args(self._overwrite_output)
        self._unfinished = []
        self._batch_meta = []
        self._batch_results = []
        self._last_pool = None
        self._mutex = Lock()

    def _task_queue(self):
        """Get the protected task queue from within the `self.last_pool`. Will error if `self.last_pool` is None."""
        return self._last_pool._taskqueue

    def _callback(self, result, callback=stack()[1][3]):
        """Wrapper to retrieve a callback matching the parent method name from `self.callbacks` if it exists.
        This is very metaprogrammed and bad practice. May be removed."""
        if callback.startswith("run_batch_"):
            callback = callback[4:]

        callback = self._callbacks.get(callback)

        if callback is not None:
            callback(result)

    def _wrap_callbacks(self, **kwargs):
        """Initialization method to wrap callbacks with required code that updates internal protected values."""
        @wraps(kwargs.get("ffprobe"))
        def _batch_ffprobe(result):
            callback = kwargs.get("ffprobe")

            with self._mutex:
                self._batch_meta = result

            if callback:
                callback(result)

        @wraps(kwargs.get("ffprobe_async"))
        def _batch_ffprobe_async(result):
            callback = kwargs.get("ffprobe_async")

            with self._mutex:
                self._batch_meta.append(result)

            if callback:
                callback(result)

        @wraps(kwargs.get("ffmpeg"))
        def _batch_ffmpeg(result):
            callback = kwargs.get("ffmpeg")

            with self._mutex:
                self._batch_results = result

            if callback:
                callback(result)

        @wraps(kwargs.get("ffmpeg_async"))
        def _batch_ffmpeg_async(result):
            callback = kwargs.get("ffmpeg_async")

            with self._mutex:
                self._batch_meta.append(result)

            if callback:
                callback(result)

        @wraps(kwargs.get("ffmpeg_gen"))
        def _batch_ffmpeg_gen(result):
            callback = kwargs.get("ffmpeg_gen")

            with self._mutex:
                self._batch_meta = result

            if callback:
                callback(result)

        @wraps(kwargs.get("ffmpeg_gen_async"))
        def _batch_ffmpeg_gen_async(result):
            callback = kwargs.get("ffmpeg_gen_async")

            with self._mutex:
                self._batch_meta.append(result)

            if callback:
                callback(result)

        kwargs.update(
            ffprobe=_batch_ffprobe,
            ffprobe_async=_batch_ffprobe_async,
            ffmpeg=_batch_ffmpeg,
            ffmpeg_async=_batch_ffmpeg_async,
            ffmpeg_gen=_batch_ffmpeg_gen,
            ffmpeg_gen_async=_batch_ffmpeg_gen_async
        )

        return kwargs

    def set_callbacks(self, **kwargs):
        """Set the callbacks by keyword arguments."""
        self._callbacks = self._wrap_callbacks(**kwargs)

    def run_batch_ffprobe(self):
        """Execute `run_ffprobe` on a batch of files synchronously, update `self.batch_meta`, and return the results."""
        with Pool(self._workers) as pool:
            self._last_pool = pool

            return pool.map_async(run_ffprobe, self._input_paths, callback=self._callback)

    def run_batch_ffprobe_async(self):
        """Execute `run_ffprobe` on a batch of files asynchronously while apppending to `self.batch_meta` and return
        the worker pool before all results are ready."""
        self._last_pool = Pool(self._workers)

        for file_path in self._input_paths:
            self._last_pool.apply_async(run_ffprobe, (file_path,), callback=self._callback)

        return self._last_pool

    def run_batch_ffmpeg(self):
        """Execute `run_ffmpeg` on a batch of files synchronously and return the results."""
        with Pool(self._workers) as pool:
            self._last_pool = pool

            return pool.map_async(utils.unzip_args(run_ffmpeg),
                                  zip(self._input_paths, self._ow_args), callback=self._callback)

    def run_batch_ffmpeg_async(self):
        """Execute `run_ffmpeg` on a batch of files asynchronously and return
        the worker pool before all results are ready."""
        self._last_pool = Pool(self._workers)

        for file_path in self._input_paths:
            self._last_pool.apply_async(run_ffmpeg, args=(file_path,),
                                        kwds=self._ow_args, callback=self._callback)

        return self._last_pool

    def run_batch_ffmpeg_gen(self):
        """Execute `run_ffmpeg_async` on a batch of files synchronously and return the results.
        Callback must be able to handle a generator."""
        with Pool(self._workers) as pool:
            self._last_pool = pool

            return pool.map_async(utils.unzip_args(run_ffmpeg_async),
                                  zip(self._input_paths, self._ow_args), callback=self._callback)

    def run_batch_ffmpeg_gen_async(self):
        """Execute `run_ffmpeg_async` on a batch of files asynchronously and return
        the worker pool before all results are ready. Callback must be able to handle a generator."""
        self._last_pool = Pool(self._workers)

        for file_path in self._input_paths:
            self._last_pool.apply_async(run_ffmpeg_async, args=(file_path,),
                                        kwds=self._ow_args, callback=self._callback)

        return self._last_pool

    def start(self, mode=7):
        """Start the conversion (collect metadata and run FFMPEG) with the callbacks specified."""
        def _ffprobe_block():
            self.run_batch_ffprobe_async()

            self._last_pool.close()
            self._last_pool.join()

        try:
            {
                0: (lambda: (self.run_batch_ffprobe(), self.run_batch_ffmpeg())),
                1: (lambda: (self.run_batch_ffprobe(), self.run_batch_ffmpeg_async())),
                2: (lambda: (self.run_batch_ffprobe(), self.run_batch_ffmpeg_gen())),
                3: (lambda: (self.run_batch_ffprobe(), self.run_batch_ffmpeg_gen_async())),
                4: (lambda: (_ffprobe_block(), self.run_batch_ffmpeg())),
                5: (lambda: (_ffprobe_block(), self.run_batch_ffmpeg_async())),
                6: (lambda: (_ffprobe_block(), self.run_batch_ffmpeg_gen())),
                7: (lambda: (_ffprobe_block(), self.run_batch_ffmpeg_gen_async())),
            }[mode]()
        except KeyError:
            raise KeyError("Mode {} does not exist. Argument 'mode' must be between 0 and 7.".format(mode))

        self._callback(self)

    def start_0(self):
        """Start with mode 0, blocking metadata collection and blocking conversion process. Uses callback keys
        `ffprobe`, `ffmpeg`, `start`, and `start_0`.
        Equivalent to `lambda: (self.start(mode=0), self._callbacks.get("start")(), self._callbacks.get("start_0")()`"""
        self.start(mode=0)
        self._callback(self)

    def start_1(self):
        """Start with mode 1, blocking metadata collection and non-blocking conversion process. Uses callback keys
        `ffprobe`, `ffmpeg`, `start`, and `start_1`.
        Equivalent to `lambda: (self.start(mode=1), self._callbacks.get("start")(), self._callbacks.get("start_1")()`"""
        self.start(mode=1)
        self._callback(self)

    def start_2(self):
        """Start with mode 2, blocking metadata collection and blocking conversion process with generator results.
        Uses callback keys `ffprobe`, `ffmpeg`, `start`, and `start_0`.
        Equivalent to `lambda: (self.start(mode=2), self._callbacks.get("start")(), self._callbacks.get("start_2")()`"""
        self.start(mode=2)
        self._callback(self)

    def start_3(self):
        """Start with mode 3, blocking metadata collection and non-blocking conversion process with generator results.
        Uses callback keys `ffprobe`, `ffmpeg`, `start`, and `start_0`.
        Equivalent to `lambda: (self.start(mode=3), self._callbacks.get("start")(), self._callbacks.get("start_3")()`"""
        self.start(mode=3)
        self._callback(self)

    def start_4(self):
        """Start with mode 0, blocking metadata collection and blocking conversion process. Uses callback keys
        `ffprobe`, `ffmpeg`, `start`, and `start_0`. Metadata collection is not internally blocking.
        Equivalent to `lambda: (self.start(mode=0), self._callbacks.get("start")(), self._callbacks.get("start_0")()`"""
        self.start(mode=4)
        self._callback(self)

    def start_5(self):
        """Start with mode 1, blocking metadata collection and non-blocking conversion process. Uses callback keys
        `ffprobe`, `ffmpeg`, `start`, and `start_1`. Metadata collection is not internally blocking.
        Equivalent to `lambda: (self.start(mode=1), self._callbacks.get("start")(), self._callbacks.get("start_1")()`"""
        self.start(mode=5)
        self._callback(self)

    def start_6(self):
        """Start with mode 2, blocking metadata collection and blocking conversion process with generator results.
        Uses callback keys `ffprobe`, `ffmpeg`, `start`, and `start_0`. Metadata collection is not internally blocking.
        Equivalent to `lambda: (self.start(mode=2), self._callbacks.get("start")(), self._callbacks.get("start_2")()`"""
        self.start(mode=6)
        self._callback(self)

    def start_7(self):
        """Start with mode 3, blocking metadata collection and non-blocking conversion process with generator results.
        Uses callback keys `ffprobe`, `ffmpeg`, `start`, and `start_0`. Metadata collection is not internally blocking.
        Equivalent to `lambda: (self.start(mode=3), self._callbacks.get("start")(), self._callbacks.get("start_3")()`"""
        self.start(mode=7)
        self._callback(self)

    def wait(self):
        """Close and join `self.last_pool`."""
        self._last_pool.close()
        self._last_pool.join()

        self._callback(self._last_pool)

    def pause(self):
        """Pause the batch operation in `self.last_pool` by adding all incomplete tasks to a protected internal field
        and empty the protected queue. Run the callback matching the name of this method. Non blocking."""
        if self._last_pool and not self._unfinished:
            queue = self._task_queue()

            with queue.mutex:
                while len(queue.queue) <= 0:
                    self._unfinished.append(queue.get())

            self._callback(self._last_pool)

    def resume(self):
        """Move all internally saved incomplete processes back into the protected queue,
        and restart and maintain workers if needed. Run the callback matching the name of this method."""
        if self._last_pool and self._unfinished:
            for task in self._unfinished:
                self._last_pool.put(task)

            self._unfinished = []

            self._last_pool._maintain_pool()

            self._callback(self._last_pool)

    def cancel(self):
        """Completely lock, clear, and close the internal protected queue of `self.last_queue` while allowing current
        workers to finish while blocking. Run the callback matching the name of this method."""
        if self._last_pool:
            queue = self._task_queue()

            with queue.mutex:
                queue.queue.clear()
                self._last_pool.close()

            self._last_pool.join()

            self._callback(self._last_pool)

    def terminate(self):
        """Terminate all workers and clear the internal incomplete list if paused."""
        if self._last_pool:
            self._last_pool.terminate()
            self._unfinished = []

            self._callback(self._last_pool)

    def get_finished(self):
        """The count of finished conversion processes."""
        return len(self._batch_meta)

    def get_unfinished(self):
        """The count of unfinished conversion processes."""
        return len(self._input_paths) - self.get_finished()
