#! /usr/bin/env python3
from utils import get_request
from qclass import QClass


class Quizlet:
    def __init__(self, client_id):
        self.client_id = client_id

    def _get_request(self, action, reps={}, params={}):
        return get_request(action, reps, {**params, "client_id": self.client_id})

    def get_class(self, class_id):
        return QClass(**self._get_request("classes.view_class", {"class_id": class_id}), __client_id=self.client_id)
