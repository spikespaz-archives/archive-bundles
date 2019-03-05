from collections import namedtuple
from datetime import datetime
from tqdm import tqdm
import requests
import click
import json


class AdoptAPI:
    adopt_api_base = "https://api.adoptopenjdk.net/v2"

    class Asset:
        VersionData = namedtuple("VersionData", "openjdk_version semver optional")

        def __init__(self, **kwargs):
            datetime_format = r"%Y-%m-%dT%H:%M:%SZ"

            self.os = kwargs.get("os", None)
            self.architecture = kwargs.get("architecture", None)
            self.binary_type = kwargs.get("binary_type", None)
            self.openjdk_impl = kwargs.get("openjdk_impl", None)
            self.binary_name = kwargs.get("binary_name", None)
            self.binary_link = kwargs.get("binary_link", None)
            self.binary_size = kwargs.get("binary_size", None)
            self.checksum_link = kwargs.get("checksum_link", None)
            self.version = kwargs.get("version", None)
            self.version_data = AdoptAPI.Asset.VersionData(
                openjdk_version=kwargs.get("version_data", dict()).get("openjdk_version", None),
                semver=kwargs.get("version_data", dict()).get("semver", None),
                optional=kwargs.get("version_data", dict()).get("optional"),
            )
            self.heap_size = kwargs.get("heap_size", None)
            self.download_count = kwargs.get("download_count", None)
            self.updated_at = wrap_throwable(
                lambda: datetime.strptime(
                    kwargs["updated_at"],
                    datetime_format),
                KeyError)()
            self.timestamp = wrap_throwable(
                lambda: datetime.strptime(
                    kwargs["timestamp"],
                    datetime_format),
                KeyError)()
            self.release_name = kwargs.get("release_name", None)
            self.release_link = kwargs.get("release_link", None)


def wrap_throwable(func, *exc):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exc:
            return None

    return wrapper
