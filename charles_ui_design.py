import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, uic, QtSerialPort, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, \
    QHBoxLayout, QStackedWidget, QAbstractButton

import pyqtgraph as pg
from settings import Settings
from params import Params

class DisplayButton(QAbstractButton):
    def __init__(self, label, value, unit, parent=None, size = (200,100)):
        super().__init__(parent)
        self.label = label
        self.value = value
        self.unit = unit
        self.size = size

    def paintEvent(self, event):
        painter = QPainter(self)

        labelFont = QFont("Times", 20, QFont.Bold)
        numberFont = QFont("Times", 36, QFont.Bold)
        unitFont =  QFont("Times", 18)

        painter.setBrush(QBrush(QColor('#d2fcdc')))
        painter.drawRect(0,0, *self.size)
        painter.setPen(QPen(QColor('#3ed5f0')))
        painter.setFont(labelFont)
        painter.drawText(self.size[0]/2.0 - 50,self.size[1]/5.0,self.label)
        painter.setPen(QPen(Qt.black))
        painter.setFont(numberFont)
        painter.drawText(self.size[0]/2.0 - 50,self.size[1]*3/5.0, str(self.value))
        painter.setFont(unitFont)
        painter.setPen(QPen(Qt.gray))
        painter.drawText(self.size[0]/2.0 - 50,self.size[1]*9/10.0, str(self.unit))

    def sizeHint(self):
        return QSize(*self.size)

class ModeButton(QAbstractButton):
    def __init__(self, label, parent=None, size = (200,50)):
        super().__init__(parent)
        self.label = label
        self.size = size

    def paintEvent(self, event):
        painter = QPainter(self)

        labelFont = QFont("Times", 20, QFont.Bold)

        painter.setBrush(QBrush(QColor('#d2fcdc')))
        painter.drawRect(0,0, *self.size)
        painter.setPen(QPen(Qt.black))
        painter.setFont(labelFont)
        painter.drawText(self.size[0]/2.0 - 50,self.size[1]*4/5.0,self.label)

    def sizeHint(self):
        return QSize(*self.size)

class DisplayRect(QWidget):
    def __init__(self, label, value, unit, parent = None, size = (200,100)):
        super().__init__(parent)
        self.label = label
        self.value = value
        self.unit = unit
        self.size = size


    def paintEvent(self, event):
        painter = QPainter(self)

        labelFont = QFont("Times", 20, QFont.Bold)
        numberFont = QFont("Times", 36, QFont.Bold)
        unitFont = QFont("Times", 18)

        painter.setBrush(QBrush(QColor('#c4dbff')))
        painter.drawRect(0, 0, *self.size)
        painter.setPen(QPen(QColor('#3ed5f0')))
        painter.setFont(labelFont)
        painter.drawText(self.size[0]/2.0 - 50, self.size[1]/5.0, self.label)
        painter.setPen(QPen(Qt.black))
        painter.setFont(numberFont)
        painter.drawText(self.size[0]/2.0 - 50, 3*self.size[1]/5.0, str(self.value))
        painter.setFont(unitFont)
        painter.setPen(QPen(Qt.gray))
        painter.drawText(self.size[0]/2.0 - 50, self.size[1]*9.0/10, str(self.unit))

    def sizeHint(self):
        return QSize(*self.size)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.settings.set_test_settings()
        self.params = Params()
        self.params.set_test_params()
        self.setFixedSize(800,480)
        self.stack = QStackedWidget(self)

        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()

        self.stack1UI()
        self.stack2UI()
        self.stack3UI()

        self.stack.addWidget(self.stack1)
        self.stack.addWidget(self.stack2)
        self.stack.addWidget(self.stack3)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.stack)

        self.setLayout(hbox)

    def stack1UI(self): #home screen
        h_box_1 = QHBoxLayout()

        v_box_1left = QVBoxLayout()
        v_box_1mid = QVBoxLayout()
        v_box_1right = QVBoxLayout()

        self.mode_main = ModeButton("MODE", size = (150,25))
        self.mode_main.clicked.connect(lambda: self.display(1))

        self.resp_rate_main = DisplayButton("Resp. Rate", self.settings.resp_rate, "b/min", size = (150,80))
        self.resp_rate_main.clicked.connect(lambda: self.display(2))

        self.tidal_vol_main = DisplayButton("Minute Volume", self.settings.minute_volume, "l/min", size = (150,80))
        #TODO: Connect this

        self.ie_main = DisplayButton("I/E Ratio", self.settings.get_ie_display(), "l/min", size = (150,80))
        # TODO: Connect this

        indices = [1,2,3,4,5,6,7]
        data = [1,2,4,5,6,8,2]
        axisStyle = {'color': 'black', 'font-size': '20pt'}

        graph_pen = pg.mkPen(width=5, color = "b")
        graph1 = pg.PlotWidget()
        graph1.setFixedWidth(400)
        graph1.plot(indices,data, pen = graph_pen)
        graph1.setBackground("w")
        graph1.setMouseEnabled(False, False)
        left1 = graph1.getAxis('left')
        left1.setLabel('Flow',**axisStyle) #TODO: Add units


        graph2 = pg.PlotWidget()
        graph2.setFixedWidth(400)
        graph2.plot(indices, data, pen = graph_pen)
        graph2.setBackground("w")
        graph2.setMouseEnabled(False, False)
        left2 = graph2.getAxis('left')
        left2.setLabel('Pressure', **axisStyle) #TODO: Add units

        graph3 = pg.PlotWidget()
        graph3.setFixedWidth(400)
        graph3.plot(indices, data, pen = graph_pen)
        graph3.setBackground("w")
        graph3.setMouseEnabled(False, False)
        left3 = graph3.getAxis('left')
        left3.setLabel('Volume', **axisStyle) #TODO: Add units

        v_box_1left.addWidget(self.mode_main)
        v_box_1left.addWidget(self.resp_rate_main)
        v_box_1left.addWidget(self.tidal_vol_main)
        v_box_1left.addWidget(self.ie_main)
        v_box_1left.addWidget(DisplayRect("PEEP", 5, "cmH2O", size = (150,80)))

        v_box_1mid.addWidget(graph1)
        v_box_1mid.addWidget(graph2)
        v_box_1mid.addWidget(graph3)

        self.tv_insp_rect = DisplayRect("TV Insp", self.params.tv_insp, "mL", size = (150,80))
        self.tv_exp_rect = DisplayRect("TV Exp", self.params.tv_exp, "mL", size = (150,80))
        self.ppeak_rect = DisplayRect("Ppeak", self.params.ppeak, "cmH2O", size=(150, 80))
        self.pplat_rect = DisplayRect("Pplat", self.params.pplat, "cmH2O", size=(150, 80))

        v_box_1right.addWidget(self.tv_insp_rect)
        v_box_1right.addWidget(self.tv_exp_rect)
        v_box_1right.addWidget(self.ppeak_rect)
        v_box_1right.addWidget(self.pplat_rect)

        h_box_1.addLayout(v_box_1left)
        h_box_1.addLayout(v_box_1mid)
        h_box_1.addLayout(v_box_1right)
        self.stack1.setLayout(h_box_1)

    def stack2UI(self):
        v_box_2 = QVBoxLayout()
        h_box_2top = QHBoxLayout()
        h_box_2bottom = QHBoxLayout()

        mode_apply = QPushButton("APPLY")
        mode_cancel = QPushButton("CANCEL")

        mode_apply.clicked.connect(self.mode_changed)
        mode_cancel.clicked.connect(lambda: self.display(0))

        h_box_2top.addWidget(QLabel("CHANGE MODE HERE"))
        h_box_2bottom.addWidget(mode_apply)
        h_box_2bottom.addWidget(mode_cancel)

        v_box_2.addLayout(h_box_2top)
        v_box_2.addLayout(h_box_2bottom)

        self.stack2.setLayout(v_box_2)

    def stack3UI(self):
        v_box_3 = QVBoxLayout()
        h_box_3top = QHBoxLayout()
        h_box_3bottom = QHBoxLayout()

        resp_rate_apply = QPushButton("APPLY")
        resp_rate_cancel = QPushButton("CANCEL")

        resp_rate_apply.clicked.connect(self.resp_rate_changed)
        resp_rate_cancel.clicked.connect(lambda: self.display(0))

        h_box_3top.addWidget(QLabel("CHANGE RESP. RATE HERE"))
        h_box_3bottom.addWidget(resp_rate_apply)
        h_box_3bottom.addWidget(resp_rate_cancel)

        v_box_3.addLayout(h_box_3top)
        v_box_3.addLayout(h_box_3bottom)

        self.stack3.setLayout(v_box_3)

    def display(self, i):
        self.stack.setCurrentIndex(i)

    def mode_changed(self):
        self.display(0)
        #TODO: Add to some sort of change list for commit

    def resp_rate_changed(self):
        self.display(0)
        #TODO: Add to some sort of change list for commit



    def update_ui(self):
        print(self.params.tv_insp)
        # TODO: Update UI elements from the params

    def open_serial(self):
        if not self.serial.isOpen():
            self.serial.open(QtCore.QIODevice.ReadWrite)

    def close_serial(self):
        if self.serial.isOpen():
            self.serial.close()

    def start_serial(self, serialport):
        self.serial = QtSerialPort.QSerialPort(
            serialport,
            baudRate=QtSerialPort.QSerialPort.Baud9600,
            readyRead=self.receive
        )
        self.open_serial()


    @QtCore.pyqtSlot()
    def receive(self):
        while self.serial.canReadLine():
            text = self.serial.readLine().data().decode()
            text = text.rstrip('\r\n')
            try:
                self.params.tv_insp = int(text)
            except:
                pass
            self.update_ui()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    #window.start_serial("/dev/cu.usbmodem143101")
    window.show()
    app.exec_()
    #window.close_serial()
    sys.exit()
    
if __name__ == '__main__':
    main()