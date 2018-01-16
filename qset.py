#! /usr/bin/env python3
from quser import QUser


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
        self.creator =          QUser(kwargs.get("creator", None)["id"])
        self.class_ids =        kwargs.get("class_ids", [])
        # self.terms =            kwargs.get("terms", [])
        # self.creator_id =       kwargs.get("creator_id", None)
