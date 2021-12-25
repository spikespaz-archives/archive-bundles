import requests


API_BASE = "https://inspirobot.me/api"


import os
import sys
import time
import random
import string

from pathlib import Path

NAME_CHARS = string.ascii_lowercase
NAME_LENGTH = 8
INTERVAL = 250
AMOUNT = 2000


def get_random_name(length=NAME_LENGTH, chars=NAME_CHARS):
    return "".join(random.choice(chars) for _ in range(length))


def get_session():
    return requests.get(f"{API_BASE}?getSessionID=1").content


def get_quotes(session_id):
    response = requests.get(f"{API_BASE}?generateFlow=1&sessionID={session_id}")

    for data in response.json().get("data"):
        if data.get("type") == "quote":
            yield data.get("text")

    yield from get_quotes(session_id)


if __name__ == "__main__":
    quotes = []

    for quote in get_quotes(get_session()):
        quotes.append(quote)
        
        print(f"{len(quotes)}/{AMOUNT}: \"{quote}\"", end="\n\n")

        filename = Path(sys.argv[1]) / (get_random_name() + ".txt")
        os.makedirs(filename.parent, exist_ok=True)

        with open(filename, "w", encoding="utf8") as file:
            file.write(quote)

        time.sleep(INTERVAL / 1000)

        if len(quotes) >= AMOUNT:
            break
