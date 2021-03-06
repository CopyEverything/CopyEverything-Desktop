from db import Database
from PyQt5.QtCore import (pyqtSignal, QObject)

class clipboardWatcher(QObject):
    on_server_update = pyqtSignal()

    def __init__(self, qtClipboard, login_callback):
        super(clipboardWatcher, self).__init__()
        self.clipboard = qtClipboard
        self._cur_contents = self.clipboard.text()
        self.clipboard.dataChanged.connect(self.update_to_server)
        self.on_server_update.connect(self.update_clipboard)
        self.first_login = True
        self.login_callback = login_callback

    def authenticate(self, username, password):
        if self.first_login:
            self.db = Database(self.login_callback, self.update_from_server)
            self.first_login = False
        self.db.authenticate(username, password)

    def update_to_server(self, replacing_paste=None):
        new_contents = self.clipboard.text()

        if new_contents != self._cur_contents:
            self.db.insert_new_paste(new_contents)
            self._cur_contents = new_contents

    def update_from_server(self, latest_paste):
        if latest_paste != self._cur_contents:
            self._cur_contents = latest_paste
            self.on_server_update.emit()
             
    def update_clipboard(self, paste = ""):
        if paste:
            self.clipboard.setText(paste)
        else:
            self.clipboard.setText(self._cur_contents)

    def get_contents(self):
        return self._cur_contents

    def stop(self):
        if not self.first_login:
            self.db.stop()

if __name__ == "__main__":
    import sys
    from PyQt5.QtCore import (QTimer)

    app = QApplication(sys.argv)
    cw = clipboardWatcher(None, None)
    timer = QTimer()
    timer.start(500)  # You may change this if you wish.
    timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms.
    sys.exit(app.exec_())
