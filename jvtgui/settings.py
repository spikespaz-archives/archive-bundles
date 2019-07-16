from pathlib import Path

import rapidjson


class SettingsFile(dict):
    def __init__(self, file_name, serialize_map=None, deserialize_map=None, defaults=None):
        self._file_name = file_name or {}
        self._serialize_map = serialize_map or {}
        self._deserialize_map = deserialize_map or {}
        self._defaults = defaults or {}

        super().__init__()

    def dump(self):
        with open(self._file_name, "w") as file:
            serialized = dict(**self)

            for key, value in serialized.items():
                serialized[key] = (
                    self._serialize_map[key](value) if key in self._serialize_map else value
                )

            rapidjson.dump(serialized, file, indent=2)

    def load(self):
        try:
            with open(self._file_name, "r") as file:
                deserialized = rapidjson.load(file)

                for key, value in deserialized.items():
                    deserialized[key] = (
                        self._deserialize_map[key](value) if key in self._deserialize_map else value
                    )

                self.update(deserialized)
                self.set_defaults()
        except (FileNotFoundError, ValueError) as error:
            print("Settings file not valid, creating default")
            print("\t", error)

            Path(self._file_name).parent.mkdir(exist_ok=True)

            self.set_defaults()
            self.dump()
            self.load()

    def set_defaults(self):
        for key, value in self._defaults.items():
            self.setdefault(key, value)
