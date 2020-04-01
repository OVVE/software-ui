import sys

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from mainwindow import UIMainWindow
from settings import AqualungSettings


class AqualungUI(QtWidgets.QMainWindow, UIMainWindow):

    def __init__(self, *args, obj=None, **kwargs):
        super(AqualungUI, self).__init__(*args, **kwargs)
        self.setup_ui(self)
        self.settings = AqualungSettings()
        self.connect()

    def connect(self):
        self.widgets.mode["button"].clicked.connect(self.mode_changed)
        self.widgets.tv["slider"].valueChanged.connect(self.tv_changed)
        self.widgets.ie["slider"].valueChanged.connect(self.ie_changed)
        self.widgets.fio2["slider"].valueChanged.connect(self.fio2_changed)
        self.widgets.resp_rate["slider"].valueChanged.connect(self.resp_rate_changed)

    def mode_changed(self):
        self.settings.mode = self.widgets.mode["button"].isChecked()  # mode = True -> AC, False -> SIMV
        if self.settings.mode:
            self.widgets.mode["button"].setText("AC")
        else:
            self.widgets.mode["button"].setText("SIMV")

    def tv_changed(self):
        self.settings.tv = self.widgets.tv["slider"].value()
        self.widgets.tv["lcd"].display(int(self.settings.tv))

    def ie_changed(self):
        self.settings.ie = self.widgets.ie["slider"].value()
        self.widgets.ie["lcd"].display(int(self.settings.ie))

    def fio2_changed(self):
        self.settings.fio2 = self.widgets.fio2["slider"].value()
        self.widgets.fio2["lcd"].display(int(self.settings.fio2))

    def resp_rate_changed(self):
        self.settings.resp_rate = self.widgets.resp_rate["slider"].value()
        self.widgets.resp_rate["lcd"].display(int(self.settings.resp_rate))


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = AqualungUI()
    screen_size = app.desktop().screenGeometry() #get the current screensize as a PyQt5 QRect
    window.resize(screen_size.width(), screen_size.height()) #resize window to screensize
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
