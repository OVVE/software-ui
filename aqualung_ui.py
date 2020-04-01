import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from mainwindow import UIMainWindow
from settings import AqualungSettings


class AqualungUi(QtWidgets.QMainWindow, UIMainWindow):

    def __init__(self, *args, obj=None, **kwargs):
        super(AqualungUi, self).__init__(*args, **kwargs)
        self.setup_ui(self)
        self.settings = AqualungSettings()
        self.connect()

    def connect(self):
        self.mode_button.clicked.connect(self.mode_changed)
        self.tv_slider.valueChanged.connect(self.tv_changed)
        self.ie_slider.valueChanged.connect(self.ie_changed)
        self.fio2_slider.valueChanged.connect(self.fio2_changed)
        self.resp_rate_slider.valueChanged.connect(self.resp_rate_changed)

    def mode_changed(self):
        self.settings.mode = self.mode_button.isChecked()  # mode = True -> AC, False -> SIMV
        if self.settings.mode:
            self.mode_button.setText("AC")
        else:
            self.mode_button.setText("SIMV")

    def tv_changed(self):
        self.settings.tv = self.tv_slider.value()
        self.tv_lcd.display(int(self.settings.tv))

    def ie_changed(self):
        self.settings.ie = self.ie_slider.value()
        self.ie_lcd.display(int(self.settings.ie))

    def fio2_changed(self):
        self.settings.fio2 = self.fio2_slider.value()
        self.fio2_lcd.display(int(self.settings.fio2))

    def resp_rate_changed(self):
        self.settings.resp_rate = self.resp_rate_slider.value()
        self.resp_rate_lcd.display(int(self.settings.resp_rate))


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = AqualungUi()
    screen_size = app.desktop().screenGeometry() #get the current screensize as a PyQt5 QRect
    window.resize(screen_size.width(), screen_size.height()) #resize window to screensize
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
