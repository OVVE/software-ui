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
from random import randint
import datetime

class FancyDisplayButton(QAbstractButton):
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
        painter.drawText(int(self.size[0]/2 - 50),int(self.size[1]/5),self.label)
        painter.setPen(QPen(Qt.black))
        painter.setFont(numberFont)
        painter.drawText(int(self.size[0]/2 - 50),int(self.size[1]*3/5), str(self.value))
        painter.setFont(unitFont)
        painter.setPen(QPen(Qt.gray))
        painter.drawText(int(self.size[0]/2 - 50),int(self.size[1]*9/10), str(self.unit))

    def sizeHint(self):
        return QSize(*self.size)

    def updateValue(self, value):
        self.value = value
        self.update()

class SimpleDisplayButton(QAbstractButton):
    def __init__(self, value, parent=None, size = (200,50)):
        super().__init__(parent)
        self.value = value
        self.size = size

    def paintEvent(self, event):
        painter = QPainter(self)

        valueFont = QFont("Times", 20, QFont.Bold)

        painter.setBrush(QBrush(QColor('#d2fcdc')))
        painter.drawRect(0,0, *self.size)
        painter.setPen(QPen(Qt.black))
        painter.setFont(valueFont)
        painter.drawText(int(self.size[0]/2 - 50),int(self.size[1]*4/5),str(self.value))

    def sizeHint(self):
        return QSize(*self.size)

    def updateValue(self, value):
        self.value = value
        self.update()


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
        painter.drawText(int(self.size[0]/2 - 50), int(self.size[1]/5), self.label)
        painter.setPen(QPen(Qt.black))
        painter.setFont(numberFont)
        painter.drawText(int(self.size[0]/2 - 50), int(3*self.size[1]/5), str(self.value))
        painter.setFont(unitFont)
        painter.setPen(QPen(Qt.gray))
        painter.drawText(int(self.size[0]/2 - 50), int(self.size[1]*9/10), str(self.unit))

    def sizeHint(self):
        return QSize(*self.size)

    def updateValue(self, value):
        self.value = value
        self.update()

class Change():
    def __init__(self, time, setting, old_val, new_val):
        self.time = time
        self.setting = setting
        self.old_val = old_val
        self.new_val = new_val

    def display(self):
        return "{}: {} changed from {} to {}".format(self.time, self.setting, self.old_val, self.new_val)

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.settings.set_test_settings()
        self.local_settings = Settings()
        self.local_settings.set_test_settings() #local settings are just changed with the UI

        self.resp_rate_increment = 0.5

        self.params = Params()
        self.params.set_test_params()

        self.mode_dict = {True: "AC", False: "SIMV"}

        self.setFixedSize(800,480) #hardcoded (non-adjustable) screensize
        self.stack = QStackedWidget(self)

        self.page1 = QWidget()
        self.page2 = QWidget()
        self.page3 = QWidget()

        self.initalizeAndAddStackWidgets()
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.stack)
        self.setLayout(hbox)


    #TODO: Add all other pages
    def initalizeAndAddStackWidgets(self):
        self.initializeWidget1()
        self.initializeWidget2()
        self.initializeWidget3()
        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)
        self.stack.addWidget(self.page3)

    def initializeWidget1(self): #home screen
        h_box_1 = QHBoxLayout()

        v_box_1left = QVBoxLayout()
        v_box_1mid = QVBoxLayout()
        v_box_1right = QVBoxLayout()

        self.mode_button_main = SimpleDisplayButton(self.mode_dict[self.settings.ac_mode], size = (150, 25))
        self.mode_button_main.clicked.connect(lambda: self.display(1))

        self.resp_rate_button_main = FancyDisplayButton("Resp. Rate", self.settings.resp_rate, "b/min", size = (150, 80))
        self.resp_rate_button_main.clicked.connect(lambda: self.display(2))

        self.tidal_vol_button_main = FancyDisplayButton("Minute Volume", self.settings.minute_volume, "l/min", size = (150, 80))
        #TODO: Connect this

        self.ie_button_main = FancyDisplayButton("I/E Ratio", self.settings.get_ie_display(), "l/min", size = (150, 80))
        # TODO: Connect this


        axisStyle = {'color': 'black', 'font-size': '20pt'}
        graph_pen = pg.mkPen(width=5, color = "b")

        self.counter = list(range(0,100))  # This is a dummy variable to graph against until we get time working
        #TODO: Figure out how to do this without "priming the pump" with a bunch of 0s
        self.tv_insp_data = [0]*100

        self.flow_graph = pg.PlotWidget()
        self.flow_graph.setFixedWidth(400)
        self.flow_graph_line = self.flow_graph.plot(self.counter,self.tv_insp_data, pen = graph_pen) #shows Serial (tv_insp) data for now
        self.flow_graph.setBackground("w")
        self.flow_graph.setMouseEnabled(False, False)
        flow_graph_left_axis = self.flow_graph.getAxis('left')
        flow_graph_left_axis.setLabel('Flow',**axisStyle) #TODO: Add units

        indices = [1,2,3,4,5,6,7,8,9, 10]
        data = [randint(-10,10) for _ in range(10)]

        self.pressure_graph = pg.PlotWidget()
        self.pressure_graph.setFixedWidth(400)
        self.pressure_graph_line = self.pressure_graph.plot(indices, data, pen = graph_pen)
        self.pressure_graph.setBackground("w")
        self.pressure_graph.setMouseEnabled(False, False)
        pressure_graph_left_axis = self.pressure_graph.getAxis('left')
        pressure_graph_left_axis.setLabel('Pressure', **axisStyle)  #TODO: Add units

        self.volume_graph = pg.PlotWidget()
        self.volume_graph.setFixedWidth(400)
        self.pressure_graph_line = self.volume_graph.plot(indices, data, pen = graph_pen)
        self.volume_graph.setBackground("w")
        self.volume_graph.setMouseEnabled(False, False)
        self.pressure_graph_left_axis = self.volume_graph.getAxis('left')
        self.pressure_graph_left_axis.setLabel('Volume', **axisStyle) #TODO: Add units

        v_box_1left.addWidget(self.mode_button_main)
        v_box_1left.addWidget(self.resp_rate_button_main)
        v_box_1left.addWidget(self.tidal_vol_button_main)
        v_box_1left.addWidget(self.ie_button_main)
        v_box_1left.addWidget(DisplayRect("PEEP", 5, "cmH2O", size = (150,80)))

        v_box_1mid.addWidget(self.flow_graph)
        v_box_1mid.addWidget(self.pressure_graph)
        v_box_1mid.addWidget(self.volume_graph)

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
        self.page1.setLayout(h_box_1)

    def initializeWidget2(self):
        v_box_2 = QVBoxLayout()
        h_box_2top = QHBoxLayout()
        h_box_2middle = QHBoxLayout()
        h_box_2bottom = QHBoxLayout()

        mode_change = SimpleDisplayButton("CHANGE MODE")
        mode_apply = SimpleDisplayButton("APPLY")
        mode_cancel= SimpleDisplayButton("Cancel")

        mode_change.clicked.connect(lambda: self.changeMode(not self.local_settings.ac_mode))
        mode_apply.clicked.connect(lambda: self.commitMode()) #TODO: fix so it updates the local setting
        mode_cancel.clicked.connect(self.cancelChange)

        self.mode_page_rect = DisplayRect("Mode", self.mode_dict[self.local_settings.ac_mode], "", size = (500,200))

        h_box_2top.addWidget(self.mode_page_rect)
        h_box_2middle.addWidget(mode_change)
        h_box_2bottom.addWidget(mode_apply)
        h_box_2bottom.addWidget(mode_cancel)

        v_box_2.addLayout(h_box_2top)
        v_box_2.addLayout(h_box_2middle)
        v_box_2.addLayout(h_box_2bottom)

        self.page2.setLayout(v_box_2)

    def initializeWidget3(self):
        v_box_3 = QVBoxLayout()
        h_box_3top = QHBoxLayout()
        h_box_3mid = QHBoxLayout()
        h_box_3bottom = QHBoxLayout()

        self.resp_rate_page_rect = DisplayRect("Resp. Rate", self.local_settings.resp_rate, "b/min", size = (500,200))

        resp_rate_increment_button = SimpleDisplayButton("+ 0.5")
        resp_rate_decrement_button = SimpleDisplayButton("- 0.5")
        resp_rate_apply = SimpleDisplayButton("APPLY")
        resp_rate_cancel = SimpleDisplayButton("CANCEL")

        resp_rate_increment_button.clicked.connect(self.incrementRespRate)
        resp_rate_decrement_button.clicked.connect(self.decrementRespRate)
        resp_rate_apply.clicked.connect(self.commitRespRate)
        resp_rate_cancel.clicked.connect(self.cancelChange)


        h_box_3top.addWidget(self.resp_rate_page_rect)
        h_box_3mid.addWidget(resp_rate_increment_button)
        h_box_3mid.addWidget(resp_rate_decrement_button)
        h_box_3bottom.addWidget(resp_rate_apply)
        h_box_3bottom.addWidget(resp_rate_cancel)

        v_box_3.addLayout(h_box_3top)
        v_box_3.addLayout(h_box_3mid)
        v_box_3.addLayout(h_box_3bottom)

        self.page3.setLayout(v_box_3)

    def display(self, i):
        self.stack.setCurrentIndex(i)

    # TODO: Add all other UI elements
    def update_ui(self):
        self.tv_insp_rect.updateValue(self.params.tv_insp)
        self.updateGraphs()

    # TODO: Polish up and process data properly
    def updateGraphs(self):
        self.counter.append(self.counter[-1] + 1)  # Add a new value 1 higher than the last.
        self.counter = self.counter[1:]  # Remove the first element.

        self.tv_insp_data.append(self.params.tv_insp)
        self.tv_insp_data = self.tv_insp_data[1:]  # Remove the first

        self.flow_graph_line.setData(self.counter, self.tv_insp_data)  # Update the data.

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
                self.parseInputAndUpdate(text)
            except:
                pass


    #TODO: Map add all other input data to proper settings
    def parseInputAndUpdate(self, text):
        self.params.tv_insp = int(text)
        #print(text)
        self.update_ui()

    # TODO: Finish all of these for each var
    def changeMode(self, new_val):
        self.local_settings.ac_mode = new_val
        self.mode_page_rect.updateValue(self.mode_dict[new_val])

    # TODO: Figure out how to handle increment properly (right now it's not in the settings)
    def incrementRespRate(self):
        self.local_settings.resp_rate+=self.resp_rate_increment
        self.resp_rate_page_rect.updateValue(self.local_settings.resp_rate)

    def decrementRespRate(self):
        self.local_settings.resp_rate-=self.resp_rate_increment
        self.resp_rate_page_rect.updateValue(self.local_settings.resp_rate)

    #TODO: Finish all of these for each var
    def commitMode(self):
        self.logChange(Change(datetime.datetime.now(),"Mode", self.mode_dict[self.settings.ac_mode], self.mode_dict[self.local_settings.ac_mode]))
        self.settings.ac_mode = self.local_settings.ac_mode
        self.mode_button_main.updateValue(self.mode_dict[self.settings.ac_mode])
        self.stack.setCurrentIndex(0)

    def commitRespRate(self):
        self.logChange(Change(datetime.datetime.now(), "Resp. Rate", self.settings.resp_rate, self.local_settings.resp_rate))
        self.settings.resp_rate = self.local_settings.resp_rate
        self.resp_rate_button_main.updateValue(self.settings.resp_rate)
        self.stack.setCurrentIndex(0)

    def changeMinuteVol(self):
        self.logChange(Change("Minute Volume", self.settings.minute_volume, self.local_settings.minute_volume))
        self.settings.minute_volume = self.local_settings.minute_volume

    def changeIERatio(self):
        #next line is designed to make sure i/e ratios are logged in readable format (not indices)
        self.logChange("I/E Ratio", self.settings.ie_ratio_display[self.settings.ie_ratio_id], self.settings.ie_ratio_display[self.local_settings.ie_ratio_id])
        self.settings.ie_ratio_id = self.local_settings.ie_ratio_id

    def cancelChange(self):
        self.local_settings = self.settings
        self.stack.setCurrentIndex(0)

    def passChanges(self, param, new_val):
        pass
        #TODO: pass settings to the Arduino

    # change is a Change object
    def logChange(self, change):
        print(change.display())
        pass
        #TODO: Actually log the change in some data structure



def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    window.start_serial("/dev/cu.usbmodem141301")
    window.show()
    app.exec_()
    window.close_serial()
    sys.exit()
    
if __name__ == '__main__':
    main()