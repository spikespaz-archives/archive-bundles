from collections import namedtuple
from datetime import datetime

import requests
import utils
import json

API_BASE_URL = "https://api.adoptopenjdk.net/v2"
STRFTIME_FORMAT = r"%Y-%m-%dT%H:%M:%SZ"


def _request(endpoint, version, nightly, **kwargs):
    request_url = "{api_base_url}/{api_endpoint}/{release_type}/{openjdk_version}".format(
        api_base_url=API_BASE_URL,
        api_endpoint=endpoint,
        release_type="nightly" if nightly else "releases",
        openjdk_version=version,
    )

    return requests.get(request_url, params=kwargs).json()


def info(version, nightly=False, **kwargs):
    response_data = _request("info", version, nightly, **kwargs)

    if kwargs.get("release") == "latest":
        yield Release(**response_data)
        raise StopIteration

    for release_data in response_data:
        yield Release(**release_data)


def binary(version, nightly=False, **kwargs):
    binary_data = _request("binary", version, nightly, **kwargs)

    return ReleaseAsset(**binary_data)


def latest_assets(version, nightly=False, **kwargs):
    response_data = _request("latestAssets", version, nightly, **kwargs)

    if kwargs.get("release") == "latest":
        yield ReleaseAsset(**response_data)
        raise StopIteration

    for asset_data in response_data:
        yield ReleaseAsset(**asset_data)


class Release:
    def __init__(self, **kwargs):
        self.release_name = kwargs.get("release_name", None)
        self.release_link = kwargs.get("release_link", None)
        self.timestamp = utils.wrap_throwable(
            lambda: datetime.strptime(kwargs["timestamp"], STRFTIME_FORMAT), KeyError
        )()
        self.release = kwargs.get("release", None)
        self.binaries = [ReleaseAsset(**data) for data in kwargs.get("binaries", list())]
        self.download_count = kwargs.get("download_count", None)

    def serialize(self):
        data = self.__dict__
        data.update(
            {
                "timestamp": self.timestamp.strftime(STRFTIME_FORMAT),
                "binaries": [binary.serialize() for binary in self.binaries],
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
        self.updated_at = utils.wrap_throwable(
            lambda: datetime.strptime(kwargs["updated_at"], STRFTIME_FORMAT), KeyError
        )()

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
                "updated_at": self.updated_at.strftime(STRFTIME_FORMAT),
            }
        )

        return data

    def json(self):
        return json.dumps(self.serialize())


class RequestOptions:
    def __init__(self, many=False, **kwargs):
        self._version = kwargs.get("_version", [] if many else None)
        self._nightly = kwargs.get("_nightly", [] if many else None)
        self.openjdk_impl = kwargs.get("openjdk_impl", [] if many else None)
        self.os = kwargs.get("os", [] if many else None)
        self.arch = kwargs.get("arch", [] if many else None)
        self.type = kwargs.get("type", [] if many else None)
        self.heap_size = kwargs.get("heap_size", [] if many else None)

    def products(self):
        for product in utils.product_dicts(**self.__dict__):
            yield RequestOptions(**product)

    def params(self):
        data = self.__dict__

        del data["_version"]
        del data["_nightly"]

        return data
