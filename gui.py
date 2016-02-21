import sys
from os import path, getcwd

from PyQt5.QtGui import QIcon, QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import (QObject, pyqtSlot, pyqtSignal,
                          QMetaObject, QVariant, Qt, Q_ARG)
from clipboardWatcher import clipboardWatcher


class QMLNameSpace(QObject):

    on_login = pyqtSignal()

    def __init__(self, engine):
        super(QMLNameSpace, self).__init__()
        self.cw = clipboardWatcher(self.login_result)
        self.engine = engine

    def login_result(self, string):
        print("got result", string)

        obj = self.engine.rootObjects()[0]
        myObj = obj.findChild(QObject, 'loginHandle')
        QMetaObject.invokeMethod(myObj, "loginResult", Qt.QueuedConnection,
                                 Q_ARG(QVariant, string))

    @pyqtSlot(str, str)
    def login(self, email, password):
        self.cw.authenticate(email, password)
        # self.on_login.emit()

    @pyqtSlot()
    def stop(self):
        self.cw.stop()
        sys.exit()

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    # add icon
    app_icon = QIcon()
    app_icon.addFile(path.join('qml', 'img', 'logo.jpg'))
    app.setWindowIcon(app_icon)

    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    py = QMLNameSpace(engine)
    ctx.setContextProperty("main", engine)
    ctx.setContextProperty("py", py)
    
    # engine.addImportPath(path.join(getcwd(), 'qml'))
    engine.setImportPathList([path.join(getcwd(), 'qml', 'lib')])
    
    engine.load('qml/gui.qml')

    window = engine.rootObjects()[0]
    window.show()

    app.aboutToQuit.connect(py.stop)
    sys.exit(app.exec_())
