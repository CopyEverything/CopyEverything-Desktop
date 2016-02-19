#!/usr/bin/env python3

import threading
from socketIO_client import SocketIO, LoggingNamespace

"""
Authentication for the SocketIO backend
"""


class Database(threading.Thread):

    def __init__(self, login_callback, fetch_callback, db_url="localhost", port=3000):
        super(Database, self).__init__()
        self.login_callback = login_callback
        self.credentials = {}
        self.online = False
        self._running = True
        self.db_url = db_url
        self.port = port

        self.sock = SocketIO(self.db_url, self.port, LoggingNamespace)

        self.sock.on('connect', self.connected)
        self.sock.on('auth resp', self.authenticate_reply)
        self.sock.on('new server copy', fetch_callback)
        self.sock.on('disconnect', self.disconnected)
        self.start()

    def good(self):
        return self.auth and self.online

    def connected(self):
        print("connected")
        self.online = True

    def disconnected(self, data):
        # attempt to reconnect on disconnect
        self.auth = False
        if self.credentials:
            self.authenticate(self.credentials['username'],
                              self.credentials['password'])

    def insert_new_paste(self, paste):
        self.sock.emit('new client copy', paste)

    def authenticate(self, user, pswd):
        if not self.connected:
            print("Not connected!")
            self.login_callback("Not connected!")

        self.credentials = {"username": user,
                            "password": pswd}
        self.sock.emit('auth', self.credentials)

    # reply will be in format: [good, str_resp (usually '')]
    def authenticate_reply(self, data):
        if data[0]:
            self.auth = True
            outcome = "good"
        else:
            outcome = "incorrect password"  # incorrect username

        self.login_callback(outcome)

    def stop(self):
        self._running = False

    def run(self):
        while(self._running):
            self.sock.wait(seconds=0.5)


if __name__ == "__main__":
    db = Database(lambda x: print(x), lambda x: print(x))
    db.authenticate("5westbury5@gmail.com", "testtest")
    db.sock.wait(1)
    db.insert_new_paste("test")
    db.sock.wait(1)
    # db.get_latest_paste()
    # db.insert_new_paste("Not last jking")
