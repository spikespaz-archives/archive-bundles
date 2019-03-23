import json
import copy

from json import JSONDecodeError


class FileDict(dict):
    def __init__(self, file, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__file = file
        self.__converters = {}

        self.__serializer = ValueSerializer()

    def dump(self):
        with open(self.__file, "w") as file:
            dictionary = self.__serializer.serialize(self)

            json.dump(dictionary, file, indent=2)

    def load(self):
        try:
            with open(self.__file, "r") as file:
                dictionary = json.load(file)
                dictionary = self.__serializer.deserialize(dictionary)

                self.update(dictionary)
        except (JSONDecodeError, FileNotFoundError) as e:
            print("Could not load settings file, creating default")
            print("\t", e)

            with open(self.__file, "w") as file:
                json.dump(self, file, indent=4)

    def serializer(self):
        return self.__serializer


class ValueSerializer:
    def __init__(self, serializers={}, deserializers={}):
        self._serializers = {}
        self._deserializers = {}

        for clazz, func in serializers:
            self.add_serializer(clazz, func)

        for name_or_type, func in deserializers:
            self.add_deserializer(name_or_type, func)

        self.add_serializer(FileDict, self._dict_serializer)
        self.add_deserializer(FileDict.__name__, self._dict_deserializer)
        self.add_serializer(dict, self._dict_serializer)
        self.add_deserializer(dict.__name__, self._dict_deserializer)
        self.add_serializer(list, self._list_serializer)
        self.add_deserializer(list.__name__, self._list_deserializer)
        self.add_serializer(tuple, self._list_serializer)
        self.add_deserializer(tuple.__name__, self._list_deserializer)

    def add_serializer(self, clazz, func):
        self._serializers[clazz] = func

    def add_deserializer(self, name, func):
        self._deserializers[name] = func

    def _dict_serializer(self, dictionary):
        for key, value in dictionary.items():
            dictionary[key] = self.serialize(value)

        return dictionary

    def _dict_deserializer(self, dictionary):
        for key, value in dictionary.items():
            dictionary[key] = self.deserialize(value)

        return dictionary

    def _list_serializer(self, iterable):
        return_list = []

        for item in list(iterable):
            return_list.append(self.serialize(item))

        return return_list

    def _list_deserializer(self, iterable):
        return_list = []

        for item in list(iterable):
            return_list.append(self.deserialize(item))

        return return_list

    def serialize(self, value):
        value = copy.deepcopy(value)

        serializer = self._serializers.get(value.__class__)

        if serializer:
            value = serializer(value)

        return value

    def deserialize(self, value):
        value = copy.deepcopy(value)

        if isinstance(value, dict):
            class_name = value.get("__class__.__name__") or value.__class__.__name__
            deserializer = self._deserializers.get(class_name)

            if deserializer:
                return deserializer(value)

        return value
