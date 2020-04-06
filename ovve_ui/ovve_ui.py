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
from display.ui_settings import (DisplayRectSettings, FancyButtonSettings,
                                 SimpleButtonSettings, TextSetting, UISettings)
from typing import Callable
from display.widgets import (initializeHomeScreenWidget, initializeModeWidget,
                             initializeRespiratoryRateWidget,
                             initializeTidalVolumeWidget,
                             initializeIERatioWidget, initializeAlarmWidget,
                             initializeGraphWidget)
from utils.params import Params
from utils.settings import Settings
from utils.alarms import Alarms
from utils.comms_adapter import CommsAdapter
from utils.comms_simulator import CommsSimulator
from utils.logger import Logger


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.settings = Settings()
        self.local_settings = Settings()  # local settings are changed with UI
        self.params = Params()

        # you can pass new settings for different object classes here
        self.ui_settings = UISettings()

        self.resp_rate_increment = 5
        self.tv_increment = 5

        # Example 1 (changes color of Fancy numbers to red)
        # self.ui_settings.set_fancy_button_settings(FancyButtonSettings(valueColor=Qt.red))
        # Example 2 (changes color of Simple numbers to red)
        # self.ui_settings.set_simple_button_settings(SimpleButtonSettings(valueColor=Qt.red))

        # Example 3 (sets display rect label font to Comic Sans MS)
        # self.ui_settings.set_display_rect_settings(DisplayRectSettings(labelSetting = TextSetting("Comic Sans MS", 20, True)))

        self.ptr = 0

        self.setFixedSize(800, 480)  # hardcoded (non-adjustable) screensize
        (layout, stack) = initializeHomeScreenWidget(self)

        self.stack = stack
        self.page = {
            "1": QWidget(),
            "2": QWidget(),
            "3": QWidget(),
            "4": QWidget(),
            "5": QWidget(),
            "6": QWidget(),
        }

        self.initalizeAndAddStackWidgets()

        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtCore.Qt.blue)
        palette.setColor(QtGui.QPalette.Background, Qt.white)
        self.setPalette(palette)

        # Instantiate the single logger for the UI
        self.logger = Logger()
        self.logger.enable_console = True

        # CommsAdapter adapts settings and params to and from the comms handler
        self.comms_adapter = CommsAdapter(self.logger)

        # Set a callback in the adapter that is called whenever new
        # params arrive from the comms handler
        self.comms_adapter.set_ui_params_callback(self.update_ui_params)

        # Set a callback in the adapter that is called whenever new
        # params arrive from the comms handler
        self.comms_adapter.set_ui_alarms_callback(self.update_ui_alarms)

        # Set the adapter function that is called whenever settings are
        # udpated in the UI
        self.set_settings_callback(self.comms_adapter.update_settings)

        # The comms handler is a simulator for now.  It will send
        # random values for the parameters that are updated periodically from
        # the MCU.  It will accept settings updates from the UI.
        #
        # When the real comms handler is available, substitute it here.
        self.comms_handler = CommsSimulator(self.comms_adapter)

        #TODO: How to handle start / stop events from UI?
        self.comms_handler.start()

    def get_mode_display(self, mode):
        switcher = {
            0: "AC",
            1: "SIMV",
        }
        return switcher.get(mode, "invalid")

    def get_ie_display(self, ie_ratio):
        switcher = {
            0: "1:1",
            1: "1:1.5",
            2: "1:2",
            3: "1:3",
        }
        return switcher.get(ie_ratio, "invalid")

    def makeFancyDisplayButton(
            self,
            label: str,
            value: Union[int, float],
            unit: str,
            size: Optional[Tuple[int, int]] = None,
            button_settings: FancyButtonSettings = None) -> FancyDisplayButton:
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
        self,
        label: str,
        size: Optional[Tuple[int, int]] = None,
        button_settings: SimpleButtonSettings = None
    ) -> SimpleDisplayButton:
        """ Creates Simple Display Button """
        return SimpleDisplayButton(
            label,
            parent=None,
            size=size,
            button_settings=self.ui_settings.simple_button_settings
            if button_settings is None else button_settings)

    def makeDisplayRect(
            self,
            label: str,
            value: Union[int, float],
            unit: str,
            size: Optional[Tuple[int, int]] = None,
            rect_settings: DisplayRectSettings = None) -> DisplayRect:
        """ Creates the Display Rectangle """
        return DisplayRect(label,
                           value,
                           unit,
                           parent=None,
                           size=size,
                           rect_settings=self.ui_settings.display_rect_settings
                           if rect_settings is None else rect_settings)

    def initalizeAndAddStackWidgets(self) -> None:
        initializeGraphWidget(self)
        initializeModeWidget(self)
        initializeRespiratoryRateWidget(self)
        initializeTidalVolumeWidget(self)
        initializeIERatioWidget(self)
        initializeAlarmWidget(self)

        for i in self.page:
            self.stack.addWidget(self.page[i])

    def display(self, i):
        self.stack.setCurrentIndex(i)

    def update_ui_params(self, params: Params) -> None:
        self.params = params
        self.updateMainDisplays()
        self.updateGraphs()

    def update_ui_alarms(self, alarms: Alarms) -> None:
        self.alarms = alarms
        print("UI received alarms from comms adapter")
        #TODO: Implement UI alarm handling

    def updateMainDisplays(self) -> None:
        self.mode_button_main.updateValue(
            self.get_mode_display(self.settings.mode))
        self.resp_rate_button_main.updateValue(self.settings.resp_rate)
        self.tv_button_main.updateValue(self.settings.tv)
        self.ie_button_main.updateValue(
            self.get_ie_display(self.settings.ie_ratio))
        self.resp_rate_display_main.updateValue(self.params.resp_rate_meas)
        self.peep_display_main.updateValue(self.params.peep)
        self.tv_insp_display_main.updateValue(self.params.tv_insp)
        self.tv_exp_display_main.updateValue(self.params.tv_exp)
        self.ppeak_display_main.updateValue(self.params.ppeak)
        self.pplat_display_main.updateValue(self.params.pplat)

    def updatePageDisplays(self) -> None:
        self.mode_page_rect.updateValue(
            self.get_mode_display(self.settings.mode))
        self.resp_rate_page_value_label.setText(str(self.settings.resp_rate))
        self.tv_page_value_label.setText(str(self.settings.tv))
        self.ie_page_rect.updateValue(
            self.get_ie_display(self.settings.ie_ratio))
        self.alarm_page_rect.updateValue(self.settings.get_alarm_display())

    # TODO: Polish up and process data properly
    def updateGraphs(self) -> None:
        self.flow_data[:-1] = self.flow_data[1:]
        self.flow_data[-1] = self.params.flow
        self.flow_graph_line.setData(self.flow_data)

        self.pressure_data[:-1] = self.pressure_data[1:]
        self.pressure_data[-1] = self.params.pressure
        self.pressure_graph_line.setData(self.pressure_data)

        self.volume_data[:-1] = self.volume_data[1:]
        self.volume_data[-1] = self.params.tv_meas
        self.volume_graph_line.setData(self.volume_data)

        self.ptr += 1
        self.flow_graph_line.setPos(self.ptr, 0)
        self.pressure_graph_line.setPos(self.ptr, 0)
        self.volume_graph_line.setPos(self.ptr, 0)

        QtGui.QApplication.processEvents()

    # TODO: Finish all of these for each var
    def changeMode(self, new_val: bool) -> None:
        self.local_settings.ac_mode = new_val
        self.mode_page_rect.updateValue(
            self.get_mode_display(self.local_settings.mode))

    # TODO: Figure out how to handle increment properly
    # (right now it's not in the settings)
    def incrementRespRate(self) -> None:
        self.local_settings.resp_rate += self.resp_rate_increment
        self.resp_rate_page_value_label.setText(
            str(self.local_settings.resp_rate))

    def decrementRespRate(self) -> None:
        self.local_settings.resp_rate -= self.resp_rate_increment
        self.resp_rate_page_value_label.setText(
            str(self.local_settings.resp_rate))

    def incrementTidalVol(self) -> None:
        self.local_settings.tv += self.tv_increment
        self.tv_page_value_label.setText(str(self.local_settings.tv))

    def decrementTidalVol(self) -> None:
        self.local_settings.tv -= self.tv_increment
        self.tv_page_value_label.setText(str(self.local_settings.tv))

    def changeIERatio(self, new_val: int) -> None:
        self.local_settings.ie_ratio = new_val
        self.ie_page_rect.updateValue(
            self.get_ie_display(self.local_settings.ie_ratio))

    def changeAlarm(self, new_val):
        self.local_settings.alarm_mode = new_val
        self.alarm_page_rect.updateValue(
            self.local_settings.get_alarm_display())

    def changeStartStop(self):
        if self.settings.run_state == 0:
            self.settings.run_state = 1
            self.start_button_main.updateValue("STOP")
            self.start_button_main.button_settings = SimpleButtonSettings(
                fillColor="#ff0000")
            self.passChanges()

        elif self.settings.run_state == 1:
            self.settings.run_state = 0
            self.start_button_main.updateValue("START")
            self.start_button_main.button_settings = SimpleButtonSettings()
            self.passChanges()

    # TODO: Finish all of these for each var
    def commitMode(self):
        self.logChange(
            Change(
                datetime.datetime.now(),
                "Mode",
                self.get_mode_display(self.settings.mode),
                self.get_mode_display(self.local_settings.mode),
            ))
        self.settings.mode = self.local_settings.mode
        self.mode_button_main.updateValue(
            self.get_mode_display(self.settings.mode))
        self.stack.setCurrentIndex(0)
        self.passChanges()
        self.updatePageDisplays()


    def commitRespRate(self) -> None:
        self.logChange(
            Change(
                datetime.datetime.now(),
                "Resp. Rate",
                self.settings.resp_rate,
                self.local_settings.resp_rate,
            ))

        self.settings.resp_rate = self.local_settings.resp_rate
        self.resp_rate_button_main.updateValue(self.settings.resp_rate)
        self.stack.setCurrentIndex(0)
        self.passChanges()
        self.local_settings = deepcopy(self.settings)
        self.updatePageDisplays()


    def commitTidalVol(self) -> None:
        self.logChange(
            Change(
                datetime.datetime.now(),
                "Tidal Vol",
                self.settings.tv,
                self.local_settings.tv,
            ))
        self.settings.tv = self.local_settings.tv
        self.tv_button_main.updateValue(self.settings.tv)
        self.stack.setCurrentIndex(0)
        self.passChanges()
        self.local_settings = deepcopy(self.settings)
        self.updatePageDisplays()


    def commitIERatio(self) -> None:
        self.logChange(
            Change(
                datetime.datetime.now(),
                "I/E Ratio",
                self.get_ie_display(self.settings.ie_ratio),
                self.get_ie_display(self.local_settings.ie_ratio),
            ))
        self.settings.ie_ratio = self.local_settings.ie_ratio
        self.ie_button_main.updateValue(
            self.get_ie_display(self.settings.ie_ratio))
        self.stack.setCurrentIndex(0)
        self.passChanges()
        self.local_settings = deepcopy(self.settings)
        self.updatePageDisplays()

    def commitAlarm(self):
        self.logChange(
            Change(datetime.datetime.now(), "Alarm acknowledged",
                   self.settings.get_alarm_display(),
                   self.local_settings.get_alarm_display()))
        self.settings.alarm_mode = self.local_settings.alarm_mode
        self.alarm_button_main.updateValue(self.settings.get_alarm_display())
        self.stack.setCurrentIndex(0)
        self.passChanges()
        self.updatePageDisplays()
        #TODO: Modify some equivalent of local settings for alarms? Not sure how this works

    def cancelChange(self) -> None:
        self.local_settings = deepcopy(self.settings)
        self.updateMainDisplays()
        self.stack.setCurrentIndex(0)
        self.updatePageDisplays()

    def passChanges(self) -> None:
        self.settings_callback(self.settings)

    def logChange(self, change: Change) -> None:
        if change.old_val != change.new_val:
            print(change.display())
        # TODO: Actually log the change in some data structure

    def set_settings_callback(
            self, settings_callback: Callable[[Settings], None]) -> None:
        self.settings_callback = settings_callback

    def closeEvent(self, *args, **kwargs):
        self.comms_handler.stop()


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
    sys.exit()


if __name__ == '__main__':
    main()
