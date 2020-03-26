import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from mainwindow import Ui_MainWindow
from settings import AqualungSettings

class AqualungUi(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, obj=None, **kwargs):
        super(AqualungUi, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.settings = AqualungSettings()
        self.connect()

    def connect(self):
        self.ac_button.clicked.connect(self.ac_changed)
        self.simv_button.clicked.connect(self.simv_changed)
        self.bpm_slider.valueChanged.connect(self.bpm_changed)
        self.tv_slider.valueChanged.connect(self.tv_changed)
        self.ie_slider.valueChanged.connect(self.ie_changed)
        self.fio2_slider.valueChanged.connect(self.fio2_changed)

    def ac_changed(self):
        self.settings.ac = self.ac_button.isChecked()
        if (self.settings.ac):
            self.ac_button.setText("AC ON")
        else:
            self.ac_button.setText("AC OFF")

    def simv_changed(self):
        self.settings.simv = self.simv_button.isChecked()
        if (self.settings.simv):
            self.simv_button.setText("SIMV ON")
        else:
            self.simv_button.setText("SIMV OFF")

    def bpm_changed(self):
        self.settings.bpm = self.bpm_slider.value()
        self.bpm_lcd.display(int(self.settings.bpm))

    def tv_changed(self):
        self.settings.tv = self.tv_slider.value()
        self.tv_lcd.display(int(self.settings.tv))

    def ie_changed(self):
        self.settings.ie = self.ie_slider.value()
        self.ie_lcd.display(int(self.settings.ie))

    def fio2_changed(self):
        self.settings.fio2 = self.fio2_slider.value()
        self.fio2_lcd.display(int(self.settings.fio2))

app = QtWidgets.QApplication(sys.argv)

window = AqualungUi()
window.show()
app.exec()


