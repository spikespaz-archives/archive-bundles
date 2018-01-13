#! /usr/bin/env python3


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
