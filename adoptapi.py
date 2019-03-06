from collections import namedtuple
from datetime import datetime

import requests
import json

api_base_url = "https://api.adoptopenjdk.net/v2"
datetime_format = r"%Y-%m-%dT%H:%M:%SZ"


def search_releases(version, nightly=False, **kwargs):
    api_url = "{api_base_url}/info/{release_type}/{openjdk_version}".format(
        api_base_url=api_base_url,
        release_type="nightly" if nightly else "releases",
        openjdk_version=version,
    )
    release_data_list = requests.get(api_url, params=kwargs).json()

    for release_data in release_data_list:
        yield Release(**release_data)


class Release:
    def __init__(self, **kwargs):
        self.release_name = kwargs.get("release_name", None)
        self.release_link = kwargs.get("release_link", None)
        self.timestamp = wrap_throwable(
            lambda: datetime.strptime(kwargs["timestamp"], datetime_format), KeyError
        )()
        self.release = kwargs.get("release", None)
        self.binaries = [ReleaseAsset(**data) for data in kwargs.get("binaries", list())]
        self.download_count = kwargs.get("download_count", None)

    def serialize(self):
        data = self.__dict__
        data.update(
            {
                "timestamp": self.timestamp.strftime(datetime_format),
                "binaries": [binary.json() for binary in self.binaries],
            }
        )

        return data

    def json(self):
        return json.dumps(self.serialize())


class ReleaseAsset:
    VersionData = namedtuple("VersionData", "openjdk_version semver optional")

    def __init__(self, **kwargs):
        self.os = kwargs.get("os", None)
        self.architecture = kwargs.get("architecture", None)
        self.binary_type = kwargs.get("binary_type", None)
        self.openjdk_impl = kwargs.get("openjdk_impl", None)
        self.binary_name = kwargs.get("binary_name", None)
        self.binary_link = kwargs.get("binary_link", None)
        self.binary_size = kwargs.get("binary_size", None)
        self.checksum_link = kwargs.get("checksum_link", None)
        self.version = kwargs.get("version", None)
        self.version_data = ReleaseAsset.VersionData(
            openjdk_version=kwargs.get("version_data", dict()).get("openjdk_version", None),
            semver=kwargs.get("version_data", dict()).get("semver", None),
            optional=kwargs.get("version_data", dict()).get("optional", None),
        )
        self.heap_size = kwargs.get("heap_size", None)
        self.download_count = kwargs.get("download_count", None)
        self.updated_at = wrap_throwable(
            lambda: datetime.strptime(kwargs["updated_at"], datetime_format), KeyError
        )()
        self.timestamp = wrap_throwable(
            lambda: datetime.strptime(kwargs["timestamp"], datetime_format), KeyError
        )()
        self.release_name = kwargs.get("release_name", None)
        self.release_link = kwargs.get("release_link", None)

    def display(self):
        return "{openjdk_impl}-{version_data.semver}-{architecture}-{binary_type}".format(
            **self.__dict__
        )

    def serialize(self):
        data = self.__dict__
        data.update(
            {
                "version_data": {
                    "openjdk_version": self.version_data.openjdk_version,
                    "semver": self.version_data.semver,
                    "optional": self.version_data.optional,
                },
                "updated_at": self.updated_at.strftime(datetime_format),
                "timestamp": self.updated_at.strftime(datetime_format),
            }
        )

        return data

    def json(self):
        return json.dumps(self.serialize())


def wrap_throwable(func, *exc):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exc:
            return None

    return wrapper
