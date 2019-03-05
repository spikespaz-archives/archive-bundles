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
            # The below lines are bugged, the default None gets passed to datetime.strptime if the keys don't exist.
            self.updated_at = datetime.strptime(kwargs.get("updated_at", None), datetime_format)
            self.timestamp = datetime.strptime(kwargs.get("timestamp", None), datetime_format)
            self.release_name = kwargs.get("release_name", None)
            self.release_link = kwargs.get("release_link", None)
