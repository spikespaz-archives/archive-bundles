import copy

from collections import namedtuple
from datetime import datetime

import requests
import rapidjson

from . import helpers

# Base URL for all AdoptOpenJDK API calls.
API_BASE_URL = "https://api.adoptopenjdk.net/v2"
# Date and time format used by AdoptOpenJDK.
STRFTIME_FORMAT = r"%Y-%m-%dT%H:%M:%SZ"


# Send a request to AdoptOpenJDK's API to retrieve JSON data for
# releases matching a Java version and a release channel.
# Optional parameters may be specified for an advanced search.
def _request(endpoint, version, nightly, **kwargs):
    release_type = "nightly" if nightly else "releases"
    request_url = f"{API_BASE_URL}/{endpoint}/{release_type}/{version}"

    request = requests.get(request_url, params=kwargs)
    request.raise_for_status()

    return request.json()


# Generator that yields multiple releases that match the current query.
def info(version, nightly=False, **kwargs):
    response_data = _request("info", version, nightly, **kwargs)

    if kwargs.get("release") == "latest":
        yield Release(**response_data)
        raise StopIteration

    for release_data in response_data:
        yield Release(**release_data)


# Returns the binary asset that most closely matches the query.
def binary(version, nightly=False, **kwargs):
    binary_data = _request("binary", version, nightly, **kwargs)

    return ReleaseAsset(**binary_data)


# Returns the latest binary asset for every matching combination of optional parameters.
def latest_assets(version, nightly=False, **kwargs):
    response_data = _request("latestAssets", version, nightly, **kwargs)

    # The returned JSON is an object, not a list. The root level is a serialized release asset.
    # In this case, the returned object must be constructed from the JSON response.
    if kwargs.get("release") == "latest":
        yield ReleaseAsset(**response_data)
        raise StopIteration

    # JSON response is a list, so yield a new object for every item (which are release assets).
    for asset_data in response_data:
        yield ReleaseAsset(**asset_data)


# Class representing the JSON data for each release returned by the API.
class Release:
    # Instantiate a release object with JSON data spread as keyword arguments.
    def __init__(self, **kwargs):
        self.release_name = kwargs.get("release_name", None)
        self.release_link = kwargs.get("release_link", None)
        self.timestamp = helpers.wrap_throwable(
            lambda: datetime.strptime(kwargs["timestamp"], STRFTIME_FORMAT), KeyError
        )()
        self.release = kwargs.get("release", None)
        binaries = kwargs.get("binaries", [])
        self.binaries = [ReleaseAsset(**binary) for binary in binaries]
        self.download_count = kwargs.get("download_count", None)

    # Serialize object data to a JSON-writable dictionary.
    def serialize(self):
        # Create a copy of this object's dictionary as to avoid mutation.
        data = copy.copy(self.__dict__)

        # Replace complex values with serializable counterparts.
        data.update(
            {
                "timestamp": self.timestamp.strftime(STRFTIME_FORMAT),
                "binaries": [binary.serialize() for binary in self.binaries],
            }
        )

        return data

    # Returns a fully serialized JSON string of object data.
    def json(self):
        return rapidjson.dumps(self.serialize())


# Class representing the JSON data for each binary asset in a release.
class ReleaseAsset:
    VersionData = namedtuple("VersionData", "openjdk_version semver optional")

    # Instantiate a binary asset from corresponding keyword arguments.
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
        self.updated_at = helpers.wrap_throwable(
            lambda: datetime.strptime(kwargs["updated_at"], STRFTIME_FORMAT), KeyError
        )()

    # Returns a human-friendly string with basic information.
    def display(self):
        return (
            f"{self.openjdk_impl}-{self.version_data.semver}-{self.architecture}-{self.binary_type}"
        )

    # Returns a fully serialized JSON string of object data.
    def serialize(self):
        # Create a copy of this object's dictionary as to avoid mutation.
        data = copy.copy(self.__dict__)

        # Replace complex values with serializable counterparts.
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

    # Returns a fully serialized JSON string of object data.
    def json(self):
        return rapidjson.dumps(self.serialize())


# Object representing all search parameters for AdoptOpenJDK's API.
class RequestOptions:
    # Constructor that can take single values for field data or
    # iterables containing several valid values for a single argument.
    def __init__(self, many=False, **kwargs):
        # The fields "_version" and "_nightly" aren't officially part of the query parameters
        # accepted by AdoptOpenJDK. They are here for reference only and must be supplied by
        # the proper named parameter for any of the request functions.
        self._version = kwargs.get("_version", [] if many else None)
        self._nightly = kwargs.get("_nightly", [] if many else None)
        self.openjdk_impl = kwargs.get("openjdk_impl", [] if many else None)
        self.os = kwargs.get("os", [] if many else None)
        self.arch = kwargs.get("arch", [] if many else None)
        self.type = kwargs.get("type", [] if many else None)
        self.heap_size = kwargs.get("heap_size", [] if many else None)

    # Yields all of the cartesian products as separate RequestOptions objects for every
    # combination of parameter values, assuming that all fields have a single value.
    def products(self):
        # No copy of this object dictionary is needed because no values are changed.
        # Check every value to make sure that it's serializable; every value must be singleton.
        for value in self.__dict__.values():
            if not isinstance(value, (tuple, list, set)):
                raise ValueError("Cannot create cartesian products from singleton values")

        # Return a new singleton RequestOptions object for every combination of dictionary value.
        for product in helpers.product_dicts(**self.__dict__):
            yield RequestOptions(**product)

    # Returns usable parameters for HTTP requests, under
    # the assumption that all fields have a single value.
    def params(self):
        # Create a copy of this object's dictionary as to avoid mutation.
        data = copy.copy(self.__dict__)

        for value in data.values():
            if isinstance(value, (tuple, list, set)):
                raise ValueError("Cannot get query parameters from a polymorphic instance")

        # Remove invalid query parameters.
        del data["_version"]
        del data["_nightly"]

        return data
