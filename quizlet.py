#! /usr/bin/env python3
import requests

from json import loads
from pathlib import Path


endpoints = loads(Path(__file__).with_name("endpoints.json").read_text())

response_codes = {
    200: "OK",
    201: "Created",
    204: "No Content",
    400: "Bad Request",
    401: "Unauthorized",
    404: "Not Found",
    405: "Method Not Allowed",
    500: "Server Error"
}


class Quizlet:
    def __init__(self, client_id):
        self.client_id = client_id

    def _get_request(self, endpoint, reps={}, params={}):
        return requests.get(endpoints["base_uri"] + endpoint.format(**reps),
                            params={**params, "client_id": self.client_id})

    def get_class(self, class_id):
        api_request = self._get_request(endpoints["classes"]["view_class"], {"class_id": class_id})

        if not api_request.ok:
            raise ConnectionError("There was an error when fetching data from: " + api_request.url +
                                  "\nError " + str(api_request.status_code) +
                                  ": " + response_codes[api_request.status_code])

        return QClass(**api_request.json())


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


class QImage:
    def __init__(self):
        self.url = ""  # _t: Thumbnail, _s: Small Square, _m: Medium, _b: Very Large, Large
        self.width = 0
        self.height = 0


class QSet:
    def __init__(self):
        self.id = 0
        self.title = ""
        self.url = ""
        self.created_by = ""
        self.created_date = ""
        self.modified_date = ""
        self.term_count = 0
        self.has_images = False
        self.visibility = ""
        self.editable = False
        self.has_access = False
        self.description = ""
        self.lang_terms = ""
        self.lang_definitions = ""
        self.terms = []


class QTerm:
    def __init__(self):
        self.id = 0
        self.term = ""
        self.definition = ""
        self.image = ""


class QSearch:
    def __init__(self):
        pass

    class QUniversalSearch:
        def __init__(self):
            self.total_results = 0
            self.total_pages = 0
            self.page = 0
            self.items = []

    class QSetSearch:
        def __init__(self):
            self.total_results = 0
            self.total_pages = 0
            self.image_set_count = 0
            self.page = 0
            self.sets = []

    class QClassSearch:
        def __init__(self):
            self.total_results = 0
            self.total_pages = 0
            self.page = 0
            self.classes = []


class QUser:
    class QStatistics:
        def __init__(self):
            self.study_session_count = 0
            self.total_answer_count = 0
            self.public_sets_created = 0
            self.public_terms_entered = 0
            self.total_sets_created = 0
            self.total_terms_entered = 0

    def __init__(self):
        self.username = ""
        self.account_type = ""
        self.sign_up_date = ""
        self.profile_image = ""
        self.statistics = QUser.QStatistics()
        self.sets = []
        self.favorite_sets = []
        self.studied = []
        self.classes = []
