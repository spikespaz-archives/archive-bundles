#! /usr/bin/env python3
import requests

from json import loads
from pathlib import Path


ENDPOINTS = loads(Path(__file__).with_name("endpoints.json").read_text())

RESPONSE_CODES = {
    200: "OK",
    201: "Created",
    204: "No Content",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Invalid Access",
    404: "Not Found",
    405: "Method Not Allowed",
    500: "Server Error"
}


def val_by_str(dictionary, key_map, sep="."):
    for key in key_map.split(sep):
        dictionary = dictionary[key]

    return dictionary


def get_request(action, reps={}, params={}):
    api_request = requests.get(ENDPOINTS["base_uri"] + val_by_str(ENDPOINTS, action).format(**reps), params=params)

    if not api_request.ok:
        raise ConnectionError("There was an error when fetching data from: " + api_request.url + "\nError " +
                              str(api_request.status_code) + ": " +
                              RESPONSE_CODES.get(api_request.status_code, "Unknown Error"))
    else:
        return api_request.json()
