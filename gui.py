#!/usr/bin/env python3

import sys
import os
from db import Database
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout,
                             QVBoxLayout, QGroupBox, QLabel, QLineEdit,
                             QPushButton, QMessageBox, QShortcut)
from PyQt5.QtGui import (QMovie, QPixmap, QKeySequence)
from PyQt5.QtCore import Qt, QSize
from ClipboardWatcher import ClipboardWatcher

"""
Implements a simple GUI that will check if something is being copy pasted.
"""


class MainWindow(QWidget):

    def __init__(self, title, w=300, h=300):
        # init QWidget Parent
        super(MainWindow, self).__init__()

        # set window props
        self.height = h
        self.width = w
        self.setFixedSize(w, h)
        self.setWindowTitle(title)

        # Start other thread
        self.cw = ClipboardWatcher(lambda x: print("change xxx:", x),
                                   self.handle_login)

        self.preload_ressources()

        # Create Window
        mainLayout = QVBoxLayout()
        self.gridGroupBox = self.createGridGroupBox()
        mainLayout.addWidget(self.gridGroupBox)
        self.setLayout(mainLayout)

        # Connections
        self.submit_button.clicked.connect(self.submitted)

        self.show()

    def preload_ressources(self):
        self.logo = QPixmap(
            os.path.join("img", "logo.png")).scaledToWidth(self.width // 2)
        self.loading_movie = QMovie(
            os.path.join("img", "loading.gif"))
        self.loading_movie.setScaledSize(QSize(self.logo.width(),
                                               self.logo.height()))

    def createGridGroupBox(self):
        gridGroupBox = QGroupBox("Copy Everything Login")
        layout = QGridLayout()
        layout.setVerticalSpacing(2)

        row = 1
        self.main_label = QLabel("Main Label")
        layout.addWidget(self.main_label, row, 0, 1, 2)
        self.main_label.setAlignment(Qt.AlignCenter)
        self.main_label.setPixmap(self.logo)

        row += 1
        self.username_field = QLineEdit()
        self.username_field.textChanged.connect(lambda:
                                                self.on_text_changed("username"))
        layout.addWidget(QLabel("Username"), row, 0)
        layout.addWidget(self.username_field, row, 1)

        row += 1
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.textChanged.connect(lambda:
                                                self.on_text_changed("password"))
        layout.addWidget(QLabel("Password"), row, 0)
        layout.addWidget(self.password_field, row, 1)

        row += 1
        self.submit_button = QPushButton("Submit")
        layout.addWidget(self.submit_button, row, 1)

        row += 1
        self.link_label = QLabel(
            "<a href='http://copyeverything.tk'>No account? Click here</a>")
        self.link_label.setOpenExternalLinks(True)
        self.link_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.link_label, row, 1)

        gridGroupBox.setLayout(layout)

        return gridGroupBox

    def submitted(self):
        username = self.username_field.text()
        password = self.password_field.text()

        if len(username) == 0 or len(password) == 0:
            if not username:
                self.username_field.setStyleSheet("background: #EEB4B4")
            if not password:
                self.password_field.setStyleSheet("background: #EEB4B4")
            return False

        self.main_label.setMovie(self.loading_movie)
        self.loading_movie.start()
        self.cw.connect(username, password)

    def handle_login(self, loginMsg):
        if loginMsg == "good":
            self.cw.collecting()
        elif "username" in loginMsg:
            self.username_field.setStyleSheet("background: #EEB4B4")
        else:
            self.password_field.setStyleSheet("background: #EEB4B4")

        self.loading_movie.stop()
        self.main_label.setPixmap(self.logo)

    def on_text_changed(self, type):
        if type == "password":
            self.password_field.setStyleSheet("background: none")
        else:
            self.username_field.setStyleSheet("background: none")

    def set_icon(self, icon_title, icon_path):
        self.setWindowTitle(icon_title)

    def paste(self):
        self.cw.update_paste()

    def stop(self):
        self.cw.stop()
        sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow("Copy Everything")
    QShortcut(QKeySequence("Ctrl+Q"), mw, mw.stop)
    QShortcut(QKeySequence("Ctrl+V"), mw, mw.paste)

    app.aboutToQuit.connect(mw.stop)
    app.exec_()
