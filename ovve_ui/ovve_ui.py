import argparse
import datetime
import os
import sys
from copy import deepcopy
from random import randint
from typing import Union, Optional, Tuple

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtSerialPort, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QAbstractButton, QApplication, QHBoxLayout,
                             QLabel, QPushButton, QStackedWidget, QVBoxLayout,
                             QWidget)

from display.button import FancyDisplayButton, SimpleDisplayButton
from display.change import Change
from display.rectangle import DisplayRect
from display.ui_settings import (DisplayRectSettings,
                                 FancyButtonSettings,
                                 SimpleButtonSettings, TextSetting,
                                 UISettings)
from utils.params import Params
from utils.settings import Settings


class MainWindow(QWidget):
    def __init__(self, debug: bool = True) -> None:
        super().__init__()
        self.settings = Settings()
        self.local_settings = Settings()  # local settings are changed with UI
        self.params = Params()

        if debug:
            self.settings.set_test_settings()
            self.local_settings.set_test_settings()
            self.params.set_test_params()

        # you can pass new settings for different object classes here
        self.ui_settings = UISettings()
        # Example 1 (changes color of Fancy numbers to red)
        # self.ui_settings.set_fancy_button_settings(FancyButtonSettings(valueColor=Qt.red))
        # Example 2 (changes color of Simple numbers to red)
        # self.ui_settings.set_simple_button_settings(SimpleButtonSettings(valueColor=Qt.red))

        # Example 3 (sets display rect label font to Comic Sans MS)
        # self.ui_settings.set_display_rect_settings(DisplayRectSettings(labelSetting = TextSetting("Comic Sans MS", 20, True)))

        self.ptr = 0

        self.setFixedSize(800, 480)  # hardcoded (non-adjustable) screensize
        self.stack = QStackedWidget(self)

        self.page = {
            "1": QWidget(),
            "2": QWidget(),
            "3": QWidget(),
            "4": QWidget(),
            "5": QWidget(),
            "6": QWidget(),
        }

        self.initalizeAndAddStackWidgets()
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.stack)
        hbox.setContentsMargins(0,0,0,0)
        self.setLayout(hbox)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtCore.Qt.blue)
        palette.setColor(QtGui.QPalette.Background, Qt.white)
        self.setPalette(palette)

    def makeFancyDisplayButton(
            self, label: str, value: Union[int, float], unit: str,
            size: Optional[Tuple[int, int]] = None,
    button_settings: FancyButtonSettings = None )-> FancyDisplayButton:
        """ Creates Fancy Display Button """
        return FancyDisplayButton(
            label,
            value,
            unit,
            parent=None,
            size=size,
            button_settings=self.ui_settings.fancy_button_settings
            if button_settings is None else button_settings)

    def makeSimpleDisplayButton(
            self, label: str,
            size: Optional[Tuple[int, int]] = None,
    button_settings: SimpleButtonSettings = None) -> SimpleDisplayButton:
        """ Creates Simple Display Button """
        return SimpleDisplayButton(
            label,
            parent=None,
            size=size,
            button_settings= self.ui_settings.simple_button_settings
            if button_settings is None else button_settings)

    def makeDisplayRect(
            self, label: str, value: Union[int, float], unit: str,
            size: Optional[Tuple[int, int]] = None,
    rect_settings: DisplayRectSettings = None) -> DisplayRect:
        """ Creates the Display Rectangle """
        return DisplayRect(
            label,
            value,
            unit,
            parent=None,
            size=size,
            rect_settings= self.ui_settings.display_rect_settings
            if rect_settings is None else rect_settings)

    def initalizeAndAddStackWidgets(self) -> None:
        self.initializeWidget1()
        self.initializeWidget2()
        self.initializeWidget3()
        self.initializeWidget4()
        self.initializeWidget5()
        self.initializeWidget6()
        
        for i in self.page:
            self.stack.addWidget(self.page[i])


    def initializeWidget1(self):  # home screen
        v_box_1_main = QVBoxLayout()

        h_box_11 = QHBoxLayout()
        h_box_12 = QHBoxLayout()

        v_box_11left = QVBoxLayout()
        v_box_11mid = QVBoxLayout()
        v_box_11right = QVBoxLayout()

        self.mode_button_main = self.makeSimpleDisplayButton(
            self.settings.get_mode_display(),
            size = (115,65),
        )
        self.mode_button_main.clicked.connect(lambda: self.display(1))

        self.set_resp_rate_button_main = self.makeFancyDisplayButton(
            "Set Resp. Rate",
            self.settings.resp_rate,
            "b/min",
            size = (115,65),
        )

        self.set_resp_rate_button_main.clicked.connect(lambda: self.display(2))

        self.set_minute_vol_button_main = self.makeFancyDisplayButton(
            "Set Minute Volume",
            self.settings.minute_volume,
            "l/min",
            size = (115,65),
        )
        self.set_minute_vol_button_main.clicked.connect(lambda: self.display(3))

        self.ie_button_main = self.makeFancyDisplayButton(
            "Set I/E Ratio",
            self.settings.get_ie_display(),
            "l/min",
            size = (115,65),
        )
        self.ie_button_main.clicked.connect(lambda: self.display(4))

        self.alarm_button_main = self.makeSimpleDisplayButton(
            "ALARM",
            size = (115,65),
            button_settings=SimpleButtonSettings(borderColor="#FF0000",
                                                 fillColor='#FFFFFF',
                                                 valueColor='#FF0000'),
        )
        self.alarm_button_main.clicked.connect(lambda: self.display(5))

        #TODO: Connect

        self.start_button_main = self.makeSimpleDisplayButton(
            "START",
            size = (115,65),
        )
        #TODO: Connect

        self.resp_rate_display_main = self.makeDisplayRect(
            "Resp. Rate",
            14,
            "bpm",
            size = (175, 115),
        )

        self.peep_display_main = self.makeDisplayRect(
            "PEEP",
            5,
            "cmH2O",
            size=(175, 115),
        )
        self.tv_insp_display_main = self.makeDisplayRect(
            "TV Insp",
            self.params.tv_insp,
            "mL",
            size=(175, 115),
        )
        self.tv_exp_display_main = self.makeDisplayRect(
            "TV Exp",
            self.params.tv_exp,
            "mL",
            size=(175, 115),
        )
        self.ppeak_display_main = self.makeDisplayRect(
            "Ppeak",
            self.params.ppeak,
            "cmH2O",
            size=(175, 115),
        )
        self.pplat_display_main = self.makeDisplayRect(
            "Pplat",
            self.params.pplat,
            "cmH2O",
            size=(175, 115),
        )

        axisStyle = {'color': 'black', 'font-size': '20pt'}
        graph_pen = pg.mkPen(width=5, color="b")

        graph_width = 400
        self.tv_insp_data = np.linspace(0, 0, graph_width)
        self.flow_graph_ptr = -graph_width

        # TODO: current graph system doesn't associate y values with x values.
        #       Need to fix?
        self.flow_graph = pg.PlotWidget()
        self.flow_graph.setFixedWidth(graph_width)
        self.flow_graph_line = self.flow_graph.plot(
            self.tv_insp_data,
            pen=graph_pen)  # shows Serial (tv_insp) data for now
        self.flow_graph.setBackground("w")
        self.flow_graph.setMouseEnabled(False, False)
        flow_graph_left_axis = self.flow_graph.getAxis("left")
        flow_graph_left_axis.setLabel("Flow", **axisStyle)  # TODO: Add units

        indices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        data = [randint(-10, 10) for _ in range(10)]

        self.pressure_graph = pg.PlotWidget()
        self.pressure_graph.setFixedWidth(graph_width)
        self.pressure_graph_line = self.pressure_graph.plot(indices,
                                                            data,
                                                            pen=graph_pen)
        self.pressure_graph.setBackground("w")
        self.pressure_graph.setMouseEnabled(False, False)
        pressure_graph_left_axis = self.pressure_graph.getAxis("left")
        pressure_graph_left_axis.setLabel("Pressure",
                                          **axisStyle)  # TODO: Add units

        self.volume_graph = pg.PlotWidget()
        self.volume_graph.setFixedWidth(graph_width)
        self.pressure_graph_line = self.volume_graph.plot(indices,
                                                          data,
                                                          pen=graph_pen)
        self.volume_graph.setBackground("w")
        self.volume_graph.setMouseEnabled(False, False)
        self.pressure_graph_left_axis = self.volume_graph.getAxis("left")
        self.pressure_graph_left_axis.setLabel("Volume",
                                               **axisStyle)  # TODO: Add units

        h_box_11.addWidget(self.mode_button_main)
        h_box_11.addWidget(self.set_resp_rate_button_main)
        h_box_11.addWidget(self.set_minute_vol_button_main)
        h_box_11.addWidget(self.ie_button_main)
        h_box_11.addWidget(self.alarm_button_main)
        h_box_11.addWidget(self.start_button_main)

        v_box_11left.addWidget(self.resp_rate_display_main)
        v_box_11left.addWidget(self.tv_insp_display_main)
        v_box_11left.addWidget(self.tv_exp_display_main)

        v_box_11mid.addWidget(self.flow_graph)
        v_box_11mid.addWidget(self.pressure_graph)
        v_box_11mid.addWidget(self.volume_graph)

        v_box_11right.addWidget(self.peep_display_main)
        v_box_11right.addWidget(self.ppeak_display_main)
        v_box_11right.addWidget(self.pplat_display_main)

        h_box_12.addLayout(v_box_11left)
        h_box_12.addLayout(v_box_11mid)
        h_box_12.addLayout(v_box_11right)

        v_box_1_main.addLayout(h_box_11)
        v_box_1_main.addLayout(h_box_12)
        self.page["1"].setLayout(v_box_1_main)

    def initializeWidget2(self):  # Mode
        v_box_2 = QVBoxLayout()
        h_box_2top = QHBoxLayout()
        h_box_2middle = QHBoxLayout()
        h_box_2bottom = QHBoxLayout()

        mode_change = self.makeSimpleDisplayButton("CHANGE MODE")
        mode_apply = self.makeSimpleDisplayButton("APPLY")
        mode_cancel = self.makeSimpleDisplayButton("CANCEL")

        mode_change.clicked.connect(
            lambda: self.changeMode(not self.local_settings.ac_mode))
        mode_apply.clicked.connect(lambda: self.commitMode())
        mode_cancel.clicked.connect(self.cancelChange)

        self.mode_page_rect = self.makeDisplayRect(
            "Mode",
            self.local_settings.get_mode_display(),
            "",
            size=(500, 200))

        h_box_2top.addWidget(self.mode_page_rect)
        h_box_2middle.addWidget(mode_change)
        h_box_2bottom.addWidget(mode_apply)
        h_box_2bottom.addWidget(mode_cancel)

        v_box_2.addLayout(h_box_2top)
        v_box_2.addLayout(h_box_2middle)
        v_box_2.addLayout(h_box_2bottom)

        self.page["2"].setLayout(v_box_2)

    def initializeWidget3(self):  # Resp_rate
        v_box_3 = QVBoxLayout()
        h_box_3top = QHBoxLayout()
        h_box_3mid = QHBoxLayout()
        h_box_3bottom = QHBoxLayout()

        self.resp_rate_page_rect = self.makeDisplayRect(
            "Resp. Rate",
            self.local_settings.resp_rate,
            "b/min",
            size=(500, 200))

        resp_rate_increment_button = self.makeSimpleDisplayButton(
            "+ " + str(self.settings.resp_rate_increment))
        resp_rate_decrement_button = self.makeSimpleDisplayButton(
            "- " + str(self.settings.resp_rate_increment))
        resp_rate_apply = self.makeSimpleDisplayButton("APPLY")
        resp_rate_cancel = self.makeSimpleDisplayButton("CANCEL")

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

        self.page["3"].setLayout(v_box_3)

    def initializeWidget4(self):  # Minute volume
        v_box_4 = QVBoxLayout()
        h_box_4top = QHBoxLayout()
        h_box_4mid = QHBoxLayout()
        h_box_4bottom = QHBoxLayout()

        self.minute_vol_page_rect = self.makeDisplayRect(
            "Minute Volume",
            self.local_settings.minute_volume,
            "l/min",
            size=(500, 200))

        minute_vol_increment_button = self.makeSimpleDisplayButton(
            "+ " + str(self.settings.minute_volume_increment))
        minute_vol_decrement_button = self.makeSimpleDisplayButton(
            "- " + str(self.settings.minute_volume_increment))
        minute_vol_apply = self.makeSimpleDisplayButton("APPLY")
        minute_vol_cancel = self.makeSimpleDisplayButton("CANCEL")

        minute_vol_increment_button.clicked.connect(self.incrementMinuteVol)
        minute_vol_decrement_button.clicked.connect(self.decrementMinuteVol)
        minute_vol_apply.clicked.connect(self.commitMinuteVol)
        minute_vol_cancel.clicked.connect(self.cancelChange)

        h_box_4top.addWidget(self.minute_vol_page_rect)
        h_box_4mid.addWidget(minute_vol_increment_button)
        h_box_4mid.addWidget(minute_vol_decrement_button)
        h_box_4bottom.addWidget(minute_vol_apply)
        h_box_4bottom.addWidget(minute_vol_cancel)

        v_box_4.addLayout(h_box_4top)
        v_box_4.addLayout(h_box_4mid)
        v_box_4.addLayout(h_box_4bottom)

        self.page["4"].setLayout(v_box_4)

    def initializeWidget5(self):  # ie ratio
        v_box_5 = QVBoxLayout()
        h_box_5top = QHBoxLayout()
        h_box_5mid = QHBoxLayout()
        h_box_5bottom = QHBoxLayout()

        self.ie_page_rect = self.makeDisplayRect(
            "I/E Ratio", self.settings.get_ie_display(), "", size=(500, 200))

        ie_change_size = (150, 50)

        ie_change_0 = self.makeSimpleDisplayButton(
            self.settings.ie_ratio_display[0], size=ie_change_size)
        ie_change_1 = self.makeSimpleDisplayButton(
            self.settings.ie_ratio_display[1], size=ie_change_size)
        ie_change_2 = self.makeSimpleDisplayButton(
            self.settings.ie_ratio_display[2], size=ie_change_size)
        ie_change_3 = self.makeSimpleDisplayButton(
            self.settings.ie_ratio_display[3], size=ie_change_size)

        ie_apply = self.makeSimpleDisplayButton("APPLY")
        ie_cancel = self.makeSimpleDisplayButton("CANCEL")

        ie_change_0.clicked.connect(lambda: self.changeIERatio(0))
        ie_change_1.clicked.connect(lambda: self.changeIERatio(1))
        ie_change_2.clicked.connect(lambda: self.changeIERatio(2))
        ie_change_3.clicked.connect(lambda: self.changeIERatio(3))

        ie_apply.clicked.connect(self.commitIERatio)
        ie_cancel.clicked.connect(self.cancelChange)

        h_box_5top.addWidget(self.ie_page_rect)
        h_box_5mid.addWidget(ie_change_0)
        h_box_5mid.addWidget(ie_change_1)
        h_box_5mid.addWidget(ie_change_2)
        h_box_5mid.addWidget(ie_change_3)

        h_box_5bottom.addWidget(ie_apply)
        h_box_5bottom.addWidget(ie_cancel)

        v_box_5.addLayout(h_box_5top)
        v_box_5.addLayout(h_box_5mid)
        v_box_5.addLayout(h_box_5bottom)

        self.page["5"].setLayout(v_box_5)

    def initializeWidget6(self): #Alarm
        v_box_6 = QVBoxLayout()
        h_box_6top = QHBoxLayout()
        #h_box_6middle = QHBoxLayout()
        h_box_6bottom = QHBoxLayout()

        alarm_ack = self.makeSimpleDisplayButton("Acknowledge")
        alarm_cancel= self.makeSimpleDisplayButton("Cancel")

        # Acknowledge alarm stops the alarms
        alarm_ack.clicked.connect(lambda: self.commitAlarm())
        alarm_cancel.clicked.connect(self.cancelChange)

        self.alarm_page_rect = self.makeDisplayRect("Alarm", self.local_settings.get_alarm_display(), "", size = (500,200))

        h_box_6top.addWidget(self.alarm_page_rect)
        #h_box_6middle.addWidget(alarm_toggle)
        h_box_6bottom.addWidget(alarm_ack)
        h_box_6bottom.addWidget(alarm_cancel)

        v_box_6.addLayout(h_box_6top)
        #v_box_6.addLayout(h_box_6middle)
        v_box_6.addLayout(h_box_6bottom)

        self.page["6"].setLayout(v_box_6)

    def display(self, i):
        self.stack.setCurrentIndex(i)

    def update_main_page_ui(self):
        self.updateMainDisplays()
        self.updateGraphs()

    def updateMainDisplays(self):
        self.mode_button_main.updateValue(self.settings.get_mode_display())
        self.set_resp_rate_button_main.updateValue(self.settings.resp_rate)
        self.set_minute_vol_button_main.updateValue(self.settings.minute_volume)
        self.ie_button_main.updateValue(self.settings.get_ie_display())
        self.alarm_button_main.updateValue(self.settings.get_alarm_display())
        self.peep_display_main.updateValue(self.params.peep)
        self.tv_insp_display_main.updateValue(self.params.tv_insp)
        self.tv_exp_display_main.updateValue(self.params.tv_exp)
        self.ppeak_display_main.updateValue(self.params.ppeak)
        self.pplat_display_main.updateValue(self.params.pplat)

    def updatePageDisplays(self):
        self.mode_page_rect.updateValue(self.settings.get_mode_display())
        self.resp_rate_page_rect.updateValue(self.settings.resp_rate)
        self.minute_vol_page_rect.updateValue(self.settings.minute_volume)
        self.ie_page_rect.updateValue(self.settings.get_ie_display())
        self.alarm_page_rect.updateValue(self.settings.get_alarm_display())

    # TODO: Polish up and process data properly
    def updateGraphs(self):
        self.tv_insp_data[:-1] = self.tv_insp_data[1:]
        self.tv_insp_data[-1] = self.params.tv_insp
        self.flow_graph_line.setData(self.tv_insp_data)
        self.ptr += 1
        self.flow_graph_line.setPos(self.ptr, 0)
        QtGui.QApplication.processEvents()

    def open_serial(self):
        if not self.serial.isOpen():
            self.serial.open(QtCore.QIODevice.ReadWrite)

    def close_serial(self):
        if self.serial.isOpen():
            self.serial.close()

    def start_serial(self, serialport):
        #TODO: error checking, retry
        self.serial = QtSerialPort.QSerialPort(
            serialport,
            baudRate=QtSerialPort.QSerialPort.Baud9600,
            readyRead=self.receive,
        )
        self.open_serial()

    @QtCore.pyqtSlot()
    def receive(self):
        while self.serial.canReadLine():
            text = self.serial.readLine().data().decode()
            text = text.rstrip("\r\n")
            try:
                self.parseInputAndUpdate(text)
            except:
                pass

    # TODO: Map add all other input data to proper settings

    def parseInputAndUpdate(self, text):
        self.params.tv_insp = int(text)
        # print(text)
        self.update_main_page_ui()

    # TODO: Finish all of these for each var
    def changeMode(self, new_val):
        self.local_settings.ac_mode = new_val
        self.mode_page_rect.updateValue(self.local_settings.get_mode_display())

    # TODO: Figure out how to handle increment properly
    # (right now it's not in the settings)
    def incrementRespRate(self):
        self.local_settings.resp_rate += self.settings.resp_rate_increment
        self.resp_rate_page_rect.updateValue(self.local_settings.resp_rate)

    def decrementRespRate(self):
        self.local_settings.resp_rate -= self.settings.resp_rate_increment
        self.resp_rate_page_rect.updateValue(self.local_settings.resp_rate)

    def incrementMinuteVol(self):
        self.local_settings.minute_volume += self.settings.minute_volume_increment
        self.minute_vol_page_rect.updateValue(
            self.local_settings.minute_volume)

    def decrementMinuteVol(self):
        self.local_settings.minute_volume -= self.settings.minute_volume_increment
        self.minute_vol_page_rect.updateValue(
            self.local_settings.minute_volume)

    def changeIERatio(self, new_val):
        self.local_settings.ie_ratio_id = new_val
        self.ie_page_rect.updateValue(self.local_settings.get_ie_display())

    def changeAlarm(self, new_val):
        self.local_settings.alarm_mode = new_val
        self.alarm_page_rect.updateValue(self.local_settings.get_alarm_display())

    # TODO: Finish all of these for each var
    def commitMode(self):
        self.logChange(
            Change(
                datetime.datetime.now(),
                "Mode",
                self.settings.get_mode_display(),
                self.local_settings.get_mode_display(),
            ))
        self.settings.ac_mode = self.local_settings.ac_mode
        self.mode_button_main.updateValue(self.settings.get_mode_display())
        self.stack.setCurrentIndex(0)

    def commitRespRate(self):
        self.logChange(
            Change(
                datetime.datetime.now(),
                "Resp. Rate",
                self.settings.resp_rate,
                self.local_settings.resp_rate,
            ))
        self.settings.resp_rate = self.local_settings.resp_rate
        self.set_resp_rate_button_main.updateValue(self.settings.resp_rate)
        self.stack.setCurrentIndex(0)

    def commitMinuteVol(self):
        self.logChange(
            Change(
                datetime.datetime.now(),
                "Minute Vol",
                self.settings.minute_volume,
                self.local_settings.minute_volume,
            ))
        self.settings.minute_volume = self.local_settings.minute_volume
        self.set_minute_vol_button_main.updateValue(self.settings.minute_volume)
        self.stack.setCurrentIndex(0)

    def commitIERatio(self):
        self.logChange(
            Change(
                datetime.datetime.now(),
                "I/E Ratio",
                self.settings.get_ie_display(),
                self.local_settings.get_ie_display(),
            ))
        self.settings.ie_ratio_id = self.local_settings.ie_ratio_id
        self.ie_button_main.updateValue(self.settings.get_ie_display())
        self.stack.setCurrentIndex(0)

    def commitAlarm(self):
        self.logChange(Change(datetime.datetime.now(),"Alarm acknowledged", self.settings.get_alarm_display(), self.local_settings.get_alarm_display()))
        self.settings.alarm_mode = self.local_settings.alarm_mode
        self.alarm_button_main.updateValue(self.settings.get_alarm_display())
        self.stack.setCurrentIndex(0)

    def cancelChange(self):
        self.local_settings = deepcopy(self.settings)
        self.updateMainDisplays()
        self.stack.setCurrentIndex(0)
        self.updatePageDisplays()

    def passChanges(self, param, new_val):
        pass
        # TODO: pass settings to the Arduino

    # change is a Change object
    def logChange(self, change):
        if change.old_val != change.new_val:
            print(change.display())
        # TODO: Actually log the change in some data structure


def main(port, argv):
    app = QApplication(argv)
    window = MainWindow()

    window.start_serial(port)
    window.show()
    app.exec_()
    window.close_serial()
    sys.exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Start the OVVE user interface')
    parser.add_argument('-p',
                        '--port',
                        help='Serial port for communication with Arduino')
    args = parser.parse_args()

    main(args.port, sys.argv)
