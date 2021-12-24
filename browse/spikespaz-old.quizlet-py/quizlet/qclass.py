#! /usr/bin/env python3
from .utils import get_request
from .qset import QSet


class QClass:
    class QSchool:
        def __init__(self, **kwargs):
            self.id =           kwargs.get("id", None)
            self.name =         kwargs.get("name", None)
            self.city =         kwargs.get("city", "")
            self.state =        kwargs.get("state", "")
            self.country_code = kwargs.get("country_code", 0)
            self.latitude =     kwargs.get("latitude", 0.0)
            self.longitude =    kwargs.get("longitude", 0.0)

    def __init__(self, **kwargs):
        self.__client_id = kwargs.get("__client_id", None)

        self.id =              kwargs.get("id", None)
        self.name =            kwargs.get("name", None)
        self.url =             kwargs.get("url", None)
        self.set_count =       kwargs.get("set_count", 0)
        self.user_count =      kwargs.get("user_count", 0)
        self.created_date =    kwargs.get("created_date", 0)
        self.has_access =      kwargs.get("has_access", False)
        self.access_level =    kwargs.get("access_level", "uninvolved")
        self.role_level =      kwargs.get("role_level", -3)
        self.description =     kwargs.get("description", "")
        self.admin_only =      kwargs.get("admin_only", True)
        self.is_public =       kwargs.get("is_public", False)
        self.has_password =    kwargs.get("has_password", False)
        self.member_add_sets = kwargs.get("member_add_sets", True)
        self.school =          QClass.QSchool(**kwargs.get("school", {}))

    def get_sets(self, client_id=None):
        if client_id is None and self.__client_id is not None:
            client_id = self.__client_id
        else:
            raise ValueError("No client ID is set, it must be set by keyword argument"
                             "during initialization or passed within the method.")

        api_request = get_request("classes.view_class_sets",
                                  reps={"class_id": self.id}, params={"client_id": client_id})

        for class_set in api_request:
            yield QSet(**class_set, __client_id=client_id)
