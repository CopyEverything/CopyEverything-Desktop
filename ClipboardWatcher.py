# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import time
import threading
import pyperclip
import sys
from db import Database


def print_to_stdout(clipboard_content):
    print("Found url: %s" % str(clipboard_content))


class ClipboardWatcher(threading.Thread):
    def __init__(self, login_callback, callback, predicate=None, pause=1.):
        super(ClipboardWatcher, self).__init__()
        self._predicate = lambda x: True if predicate is None else predicate
        self._callback = callback
        self._login_callback = login_callback
        self._pause = pause
        self._stopping = False
        self._collecting = False
        self.alive = False
        self.recent_value = pyperclip.paste()
        self.db = Database()
        self._cv = threading.Condition()
        self.begin()

    def run(self):
        with self._cv:
            while not self._stopping:
                if self._collecting:
                    tmp_value = pyperclip.paste()
                    if tmp_value != self.recent_value:
                        self.update_paste()
                        if self._predicate(self.recent_value):
                            self._callback(self.recent_value)
                    else:
                        self.update_copy()
                if self.db.credentials:
                    self.login()
                self._cv.wait_for(self.stopping, timeout=self._pause)

    def collecting(self):
        self._collecting = True

    def begin(self):
        if not self.alive:
            self.start()
            self.alive = True

    def stop(self):
        if self.alive:
            self._stopping = True
            self.alive = False

    def stopping(self):
        return self._stopping

    def connect(self, username, password):
        self.db.connect(username, password)

    def update_paste(self, replacing_paste=None):
        if replacing_paste is None:
            replacing_paste = str(pyperclip.paste())

        if replacing_paste != self.recent_value:
            self.db.insert_new_paste(replacing_paste)
            self.recent_value = replacing_paste

    def update_copy(self):
        latest_paste = str(self.db.get_latest_paste())
        if latest_paste != self.recent_value:
            print("updating with", latest_paste.encode(sys.stdout.encoding, errors='replace'))
            pyperclip.copy(latest_paste)
            self.recent_value = latest_paste

    def login(self):
        res = self.db.authenticate()
        self._login_callback(res)
         
    def get_contents(self):
        return self.recent_value

if __name__ == "__main__":
    cw = ClipboardWatcher(print_to_stdout, 5.)
    cw.start()
    while 1:
        try:
            print("Waiting for changed clipboard...")
            time.sleep(10)
        except KeyboardInterrupt:
            cw.stop()
            break
    # cw.run()
