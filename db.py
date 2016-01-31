#!/usr/bin/env python3

import requests
import json
from time import time

"""
Authentication for the Firebase backend
"""


class Database():

    def __init__(self, callback, db_url="https://vivid-inferno-6279.firebaseio.com"):
        self.alive = False
        self.callback = callback
        self.credentials = {}
        self.userid = -1
        self.latest_paste_num = -1
        self.db_url = db_url
        self.token = ""
        self.db = None

    def connect(self, user, pswd):
        self.credentials = {"username": user, "password": pswd}

    def insert_empty_row(self):
        url = self.db_url + "/copies.json?auth=" + self.token
        new_dict = {self.userid: []}

        try:
            requests.put(url, data=json.dumps(new_dict))
        except requests.exceptions.ConnectionError:
            pass

    def insert_new_paste(self, paste):
        url = self.db_url + "/copies/" + \
            str(self.userid) + ".json?auth=" + self.token
        self.get_latest_paste()  # update the latest paste number

        new_paste = {self.latest_paste_num: {"content": paste,
                                             "timestamp": int(time())}}
        try:
            requests.patch(url, data=json.dumps(new_paste))
        except requests.exceptions.ConnectionError:
            pass

    def get_latest_paste(self):
        self.latest_paste_num = 0
        url = self.db_url + "/copies/" + str(self.userid) +\
            ".json?orderBy=\"$key\"&auth=" + self.token

        try:
            r = requests.get(url)
        except requests.exceptions.ConnectionError:
            r = "[]"

        json_list = json.loads(r.text)

        if json_list:
            latest_paste = json_list[-1]
            self.latest_paste_num = len(json_list)
            return latest_paste["content"]
        else:
            self.insert_empty_row()
            return ""

    def authenticate(self):
        outcome = "incorrect password"
        email, pas = self.credentials["username"], self.credentials["password"]
        self.credentials = {}

        try:
            r = requests.post(
                "http://copyeverything.tk/auth.php", {"email": email,
                                                      "pass": pas})
        except requests.exceptions.ConnectionError:
            self.callback(outcome)
            return

        json_reply = json.loads(r.text)

        if r.status_code == 200 and json_reply[0]:
            outcome = "good"
            self.userid = json_reply[1]
            self.token = json_reply[2]

        elif "username" in json_reply[1] or "email" in json_reply[1]:
            outcome = "incorrect username"

        self.callback(outcome)


if __name__ == "__main__":
    db = Database(lambda x: print(x))
    db.connect("nico@test.com", "testtest")
    db.authenticate()
    db.get_latest_paste()
    db.insert_new_paste("Not last jking")
