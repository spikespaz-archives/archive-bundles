from pathlib import Path

import rapidjson


class SettingsFile(dict):
    def __init__(self, file_name, serialize_map=None, deserialize_map=None, defaults=None):
        self._file_name = file_name or {}
        self._serialize_map = serialize_map or {}
        self._deserialize_map = deserialize_map or {}
        self._defaults = defaults or {}

        super().__init__()

    def dump(self, debug=False):
        if debug:
            self.debug_dump()

            return

        with open(self._file_name, "w") as file:
            serialized = dict(**self)

            for key, value in serialized.items():
                serialized[key] = (
                    self._serialize_map[key](value) if key in self._serialize_map else value
                )

            rapidjson.dump(serialized, file, indent=2)

            return serialized

    def debug_dump(self):
        import builtins

        old_dict = None
        
        with open(self._file_name, "r") as file:
            old_dict = rapidjson.load(file)

        new_dict = self.dump()

        new_dict_keys = list(new_dict.keys())
        old_dict_keys = list(old_dict.keys())

        for key in new_dict_keys + old_dict_keys:
            if key in new_dict_keys and key not in old_dict_keys:
                print(f"[A] {key}: {new_dict[key].__repr__()}")

                continue
            if key in new_dict_keys and old_dict_keys:
                if old_dict[key] == new_dict[key]:
                    continue

                print(f"[U] {key}: {old_dict[key].__repr__()} => {new_dict[key].__repr__()}")

                continue
            if key in old_dict_keys and key not in new_dict_keys:
                print(f"[D] {key}: {old_dict[key].__repr__()}")

                continue

        return new_dict

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
