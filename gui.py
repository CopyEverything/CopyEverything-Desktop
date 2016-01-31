# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import sys
import os
from primary_widget import PrimaryWidget
from PyQt5.QtWidgets import (QApplication, QShortcut, QMainWindow, QAction)
from PyQt5.QtGui import (QKeySequence, QIcon)
from PyQt5.QtCore import Qt


"""
Implements a simple GUI that will check if something is being copy pasted.
"""


class MainWindow(QMainWindow):

    def __init__(self, title, w=300, h=330):
        super(MainWindow, self).__init__()
        self.height = h
        self.width = w
        self.setFixedSize(w, h)
        self.setWindowTitle(title)
        self.widget = PrimaryWidget(w, h)
        self.setCentralWidget(self.widget)

        self.copyAct = QAction("&Copy", self, shortcut=QKeySequence.Copy,
                               statusTip="Copy the current selection's contents to the clipboard",
                               triggered=self.copy)
        self.pasteAct = QAction("&Paste", self, shortcut=QKeySequence.Paste,
                                statusTip="Paste the clipboard's contents into the current selection",
                                triggered=self.paste)
        self.quitAct = QAction("&Quit", self, shortcut=QKeySequence("Ctrl+Q"),
                               statusTip="Quit the program",
                               triggered=self.stop)
        self.submitAct = QAction("&Submit", self, shortcut=QKeySequence(Qt.Key_Return),
                                 statusTip="Submit the form", triggered=self.widget.submitted)

        self.fileMenu = self.menuBar().addMenu("&Edit")
        self.fileMenu.addAction(self.copyAct)
        self.fileMenu.addAction(self.pasteAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.submitAct)
        self.fileMenu.addAction(self.quitAct)

        self.show()

    def set_icon(self, icon_title, icon_path):
        self.setWindowTitle(icon_title)
        self.setWindowIcon(QIcon(icon_path))

    def paste(self):
        print("Pasting")
        self.widget.paste()

    def copy(self):
        # get copy from db...
        print("Copying")
        self.widget.copy()

    def stop(self):
        self.widget.stop()
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow("Copy Everything")
    main.set_icon("Copy Everything", os.path.join("img", "logo.svg"))

    app.aboutToQuit.connect(main.stop)
    app.exec_()
