#!/usr/bin/env python3

from firebase import firebase
from time import sleep

"""
Authentication for the Firebase backend
"""


class Database():

    def __init__(self, callback, db_url="https://vivid-inferno-6279.firebaseio.com"):
        self.fb = firebase.FirebaseApplication(db_url, authentication=None)
        # authentication = firebase.Authentication(
        #     'MpOarmTxyqTek2HZAot6Gjc1jmMpapxTBo70cqF2', '5westbury5@gmail.com')
        # self.fb.authentication = authentication
        # print(authentication.extra)

        self.alive = False
        self.callback = callback
        self.credentials = {}

    def connect(self, user, pswd):
        self.credentials = {"username": user, "password": pswd}

    def authenticate(self):
        outcome = "incorrect password"
        try:
            result = self.fb.get('/users', self.credentials["username"])
        except:  # if internet connection was lost or server is not working
            result = None

        if result is None:
            outcome = "incorrect username"
        elif result == self.credentials["password"]:
            outcome = "good"

        print("Authenticated", outcome)
        self.callback(outcome)
        self.credentials = {}


if __name__ == "__main__":
    db = Database()
