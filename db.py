#!/usr/bin/env python3

import requests
import json
import random
import string
from time import time

"""
Authentication for the Firebase backend
"""


class Database():

    def __init__(self, db_url="https://vivid-inferno-6279.firebaseio.com"):
        self.alive = False
        self.credentials = {}
        self.userid = -1
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
        
        chars = string.ascii_uppercase + string.digits
        rnd_string = ''.join(random.choice(chars) for _ in range(10))
        new_paste = {"content": paste, "timestamp": int(time())}
        try:
            requests.post(url, data=json.dumps(new_paste))
        except requests.exceptions.ConnectionError:
            pass

    def get_latest_paste(self):
        url = self.db_url + "/copies/" + str(self.userid) +\
            ".json?orderBy=\"timestamp\"&limitToLast=1&auth=" + self.token

        try:
            r = requests.get(url)
            json_el = json.loads(r.text)
        except requests.exceptions.ConnectionError:
            json_el = False

        if json_el:
            return json_el.popitem()[1]["content"]
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
            return outcome

        json_reply = json.loads(r.text)

        if r.status_code == 200 and json_reply[0]:
            outcome = "good"
            self.userid = json_reply[1]
            self.token = json_reply[2]

        elif "username" in json_reply[1] or "email" in json_reply[1]:
            outcome = "incorrect username"

        return outcome


if __name__ == "__main__":
    db = Database(lambda x: print(x))
    db.connect("nico@test.com", "testtest")
    db.authenticate()
    db.get_latest_paste()
    db.insert_new_paste("Not last jking")
