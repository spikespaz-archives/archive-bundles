#! /usr/bin/env python3


endpoints = {
    "classes": {
        "view_class": "/classes/{class_id}",
        "view_class_sets": "/classes/{class_id}/sets",
        "add_class": "/classes",
        "edit_class": "/classes/{class_id}",
        "delete_class": "/classes/{class_id}",
        "add_class_set": "/classes/{class_id}/sets/{set_id}",
        "remove_class_set": "/classes/{class_id}/sets/{set_id}",
        "join_class": "/classes/{class_id}/members/{username}",
        "leave_class": "/classes/{class_id}/members/{username}"
    },
    "images": {
        "upload_image": "/images"
    },
    "search": {
        "search_sets": "/search/sets",
        "search_classes": "/search/classes",
        "search_universal": "/search/universal"
    },
    "sets": {
        "view_set": "/sets/{set_id}",
        "view_set_terms": "/sets/{set_id}/terms",
        "submit_password": "/sets/{set_id}/password",
        "view_random_sets": "/sets",
        "view_all_class_sets": "/classes/{class_id}/sets",
        "view_all_user_sets": "/users/{username}/sets",
        "view_all_user_favorite_sets": "/users/{username}/favorites",
        "add_set": "/sets",
        "edit_set": "/sets/{set_id}",
        "delete_set": "/sets/{set_id}",
        "add_set_term": "/sets/{set_id}/terms",
        "edit_set_term": "/sets/{set_id}/terms/{term_id}",
        "delete_set_term": "/sets/{set_id}/terms/{term_id}"
    },
    "users": {
        "view_user": "/users/{username}",
        "view_user_sets": "/users/{username}/sets",
        "view_user_favorites": "/users/{username}/favorites",
        "view_user_classes": "/users/{username}/classes",
        "view_recently_studied": "/users/{username}/studied",
        "add_favorite_set": "/users/{username}/favorites/{set_id}",
        "remove_favorite_set": "/users/{username}/favorites/{set_id}"
    }
}


class Quizlet:
    def __init__(self, api_key="", base_uri="https://api.quizlet.com/2.0"):
        self.api_key = api_key
        self.base_uri = base_uri


class QClass:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.set_count = 0
        self.user_count = 0
        self.created_date = ""
        self.admin_only = False
        self.has_access = False
        self.access_level = ""
        self.description = ""
        self.sets = []
        self.members = []


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
