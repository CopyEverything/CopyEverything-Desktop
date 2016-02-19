#!/usr/bin/env python3

import os
from PyQt5.QtWidgets import (QWidget, QGridLayout, QVBoxLayout,
                             QGroupBox, QLabel, QLineEdit,
                             QPushButton)
from PyQt5.QtCore import (Qt, QSize, pyqtSignal)
from PyQt5.QtGui import (QMovie, QPixmap)
from ClipboardWatcher import ClipboardWatcher


class PrimaryWidget(QWidget):
    login_trigger = pyqtSignal()

    def __init__(self, w, h):
        # Init QWidget Parent
        super(PrimaryWidget, self).__init__()

        # Set window props
        self.height = h
        self.width = w
        self.setFixedSize(w, h)
        self.logged_in = False

        # Load images etc.
        self.preload_ressources()

        self.login_trigger.connect(self.login)
        self.login_msg = ""

        self.cw = ClipboardWatcher(self.handle_login)

        # Create Window
        mainLayout = QVBoxLayout()
        self.gridGroupBox = self.createGridGroupBox()
        mainLayout.addWidget(self.gridGroupBox)
        self.setLayout(mainLayout)

        # Connections
        self.submit_button.clicked.connect(self.submitted)

    def preload_ressources(self):
        self.logo = QPixmap(
            os.path.join("img", "logo.png")).scaledToWidth(self.width // 2 - 10)
        self.loading_movie = QMovie(
            os.path.join("img", "loading.gif"))
        self.loading_movie.setScaledSize(QSize(self.logo.width() - 30,
                                               self.logo.height() - 30))

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

        if not self.logged_in and len(username) == 0 or len(password) == 0:
            if not username:
                self.username_field.setStyleSheet("background: #EEB4B4")
            if not password:
                self.password_field.setStyleSheet("background: #EEB4B4")
            return False

        self.submit_button.setEnabled(False)
        self.main_label.setMovie(self.loading_movie)
        self.loading_movie.start()
        self.cw.authenticate(username, password)

    def handle_login(self, loginMsg):
        self.login_msg = loginMsg
        self.login_trigger.emit()

    def login(self):
        if self.login_msg == "good":
            self.username_field.setText("")
            self.password_field.setText("")
            self.username_field.setReadOnly(True)
            self.password_field.setReadOnly(True)
            self.username_field.setStyleSheet("background: #7DDB7D")
            self.password_field.setStyleSheet("background: #7DDB7D")
            self.submit_button.setEnabled(False)
            self.logged_in = True
        elif "username" in self.login_msg:
            self.username_field.setStyleSheet("background: #EEB4B4")
        else:
            self.password_field.setStyleSheet("background: #EEB4B4")

        self.loading_movie.stop()
        self.main_label.setPixmap(self.logo)

    def on_text_changed(self, type):
        if not self.logged_in:
            self.submit_button.setEnabled(True)
            if type == "password":
                self.password_field.setStyleSheet("background: none")
            else:
                self.username_field.setStyleSheet("background: none")

    def stop(self):
        self.cw.stop()
