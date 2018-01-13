#! /usr/bin/env python3


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
