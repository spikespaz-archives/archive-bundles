#! /usr/bin/env python3


class QUser:
    class QStatistics:
        def __init__(self, **kwargs):
            self.study_session_count = kwargs.get("study_session_count", 0)
            self.total_answer_count = kwargs.get("total_answer_count", 0)
            self.public_sets_created = kwargs.get("public_sets_created", 0)
            self.public_terms_entered = kwargs.get("public_terms_entered", 0)

    def __init__(self, **kwargs):
        self.username =      kwargs.get("username", None)
        self.account_type =  kwargs.get("account_type", "free")
        self.profile_image = kwargs.get("profile_image", None)
        self.id =            kwargs.get("id", None)
        self.statistics =    QUser.QStatistics(**kwargs.get("statistics", {}))
        self.sign_up_date =  kwargs.get("sign_up_date", 0)
        # self.sets =          kwargs.get("sets", [])
        # self.studied =       kwargs.get("studied", [])
        # self.groups =        kwargs.get("groups", [])
