import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from testwindow import Ui_MainWindow
from test_settings import TestSettings

class test_ui(QtWidgets.QMainWindow, Ui_MainWindow):
    full = True

    def __init__(self, *args, obj=None, **kwargs):
        super(test_ui, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.settings = TestSettings()
        self.connect()

    def connect(self):
        self.main_peep.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.main_fio2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.fio2_main.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        self.fio2_lcd.display(self.settings.fio2)
        self.fio2_page_lcd.display(self.settings.page_fio2)


        self.fio2_up.clicked.connect(self.fio2_incremented)
        self.fio2_down.clicked.connect(self.fio2_decremented)

    def fio2_incremented(self):
        print("Initial", self.settings.page_fio2)
        print("increment", self.settings.fio2_inc)
        self.settings.page_fio2 = self.settings.page_fio2 + self.settings.fio2_inc
        print("Final", self.settings.page_fio2)
        self.fio2_page_lcd.display(self.settings.page_fio2)


    def fio2_decremented(self):
        print("Initial", self.settings.page_fio2)
        print("decrement", self.settings.fio2_inc)
        self.settings.page_fio2 = self.settings.page_fio2 - self.settings.fio2_inc
        print("Final", self.settings.page_fio2)

        self.fio2_page_lcd.display(self.settings.page_fio2)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.hide()
            if self.full:
                self.showNormal()
                self.full = False
            elif not self.full:
                self.showFullScreen()
                self.full = True

app = QtWidgets.QApplication(sys.argv)

window = test_ui()
screen_size = app.desktop().screenGeometry() #get the current screensize as a PyQt5 QRect
window.showFullScreen()
app.exec()


