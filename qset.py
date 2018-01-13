#! /usr/bin/env python3


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
