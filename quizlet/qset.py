#! /usr/bin/env python3
from .utils import get_request
from .quser import QUser


class QSet:
    def __init__(self, **kwargs):
        self.__client_id = kwargs.get("__client_id", None)

        self.id =               kwargs.get("id", None)
        self.url =              kwargs.get("url", None)
        self.title =            kwargs.get("title", None)
        self.created_by =       kwargs.get("created_by", "")
        self.term_count =       kwargs.get("term_count", 0)
        self.created_date =     kwargs.get("created_date", 0)
        self.modified_date =    kwargs.get("modified_date", 0)
        self.published_date =   kwargs.get("published_date", 0)
        self.has_images =       kwargs.get("has_images", False)
        self.subjects =         kwargs.get("subjects", [])
        self.visibility =       kwargs.get("visibility", "public")
        self.editable =         kwargs.get("editable", "only_me")
        self.has_access =       kwargs.get("has_access", True)
        self.can_edit =         kwargs.get("can_edit", False)
        self.description =      kwargs.get("description", "")
        self.lang_terms =       kwargs.get("lang_terms", "en")
        self.lang_definitions = kwargs.get("lang_definitions", "en")
        self.password_use =     kwargs.get("password_use", 0)
        self.password_edit =    kwargs.get("password_edit", 0)
        self.access_type =      kwargs.get("access_type", 2)
        # self.creator =          QUser(**kwargs.get("creator", {}))
        self.class_ids =        kwargs.get("class_ids", [])
        # self.terms =            kwargs.get("terms", [])
        self.creator_id =       kwargs.get("creator_id", None)
        self.creator_name =     kwargs.get("creator", {"username": None})["username"]

    def get_creator(self, client_id=None):
        if client_id is None and self.__client_id is not None:
            client_id = self.__client_id
        else:
            raise ValueError("No client ID is set, it must be set by keyword argument"
                             "during initialization or passed within the method.")

        return QUser(**get_request("users.view_user",
                                   reps={"username": self.creator_name}, params={"client_id": client_id}))

    def get_terms(self, client_id=None):
        if client_id is None and self.__client_id is not None:
            client_id = self.__client_id
        else:
            raise ValueError("No client ID is set, it must be set by keyword argument"
                             "during initialization or passed within the method.")

        api_request = get_request("sets.view_set_terms", reps={"set_id": self.id}, params={"client_id": client_id})

        for class_set in api_request:
            yield QSet(**class_set, __client_id=client_id)
