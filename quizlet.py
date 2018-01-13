#! /usr/bin/env python3
from json import loads
from pathlib import Path
from requests import request

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
    def __init__(self, api_key="", base_uri="https://api.quizlet.com/2.0"):
        self.api_key = api_key
        self.base_uri = base_uri


class QClass:
    def __init__(self, class_id, base_uri="https://api.quizlet.com/2.0"):
        api_request = request.get(base_uri + endpoints["view_class"].format(class_id=class_id))

        if not api_request.ok:
            raise ConnectionError("There was an error (" + str(api_request.status_code) +
                                  ") when fetching data from: " + api_request.url)

        self.request = api_request

        api_request_json = api_request.json()

        self.id = api_request_json["id"]
        self.name = api_request_json["name"]
        # self.set_count = api_request_json["set_count"]
        # self.user_count = api_request_json["user_count"]
        self.created_date = api_request_json["created_date"]
        self.admin_only = api_request_json["admin_only"]
        self.has_access = api_request_json["has_access"]
        self.access_level = api_request_json["access_level"]
        self.description = api_request_json["description"]
        self.sets = [class_set["id"] for class_set in api_request_json["sets"]]
        self.members = [class_set["id"] for class_set in api_request_json["members"]]


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
    def __init__(self):
        self.username = ""
        self.account_type = ""
        self.sign_up_date = ""
        self.profile_image = ""
        self.statistics = QStatistics()
        self.sets = []
        self.favorite_sets = []
        self.studied = []
        self.classes = []


class QStatistics:
    def __init__(self):
        self.study_session_count = 0
        self.total_answer_count = 0
        self.public_sets_created = 0
        self.public_terms_entered = 0
        self.total_sets_created = 0
        self.total_terms_entered = 0
