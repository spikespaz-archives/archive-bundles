import json

from json import JSONDecodeError
from pathlib import Path


class SettingsFile(dict):
    def __init__(self, file_name, serialize_map={}, deserialize_map={}, defaults={}):
        self._file_name = file_name
        self._serialize_map = serialize_map
        self._deserialize_map = deserialize_map
        self._defaults = defaults

    def dump(self):
        with open(self._file_name, "w") as file:
            serialized = dict(**self)

            for key, value in serialized.items():
                serialized[key] = self._serialize_map[key](value)

            json.dump(serialized, file, indent=2)

    def load(self):
        try:
            with open(self._file_name, "r") as file:
                deserialized = json.load(file)

                for key, value in deserialized.items():
                    deserialized[key] = self._deserialize_map[key](value)

                self.update(deserialized)
                self.set_defaults()
        except (FileNotFoundError, JSONDecodeError) as e:
            print("Settings file not valid, creating default")
            print("\t", e)

            Path(self._file_name).parent.mkdir(exist_ok=True)

            self.set_defaults()
            self.dump()
            self.load()

    def set_defaults(self):
        for key, value in self._defaults.items():
            self.setdefault(key, value)
