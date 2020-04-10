import argparse
import datetime
import json
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
                             QWidget, QMessageBox, QDialog)

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
from utils.comms_simulator import CommsSimulator
from utils.comms_link import CommsLink
from utils.logger import Logger


class MainWindow(QWidget):
    new_settings_signal = pyqtSignal(dict)

    def __init__(self, is_sim: bool=False) -> None:
        super().__init__()
        self.settings = Settings()
        self.local_settings = Settings()  # local settings are changed with UI
        self.params = Params()
        
        
        self.fullscreen = False

        # you can pass new settings for different object classes here
        self.ui_settings = UISettings()

        self.resp_rate_increment = 1
        self.tv_increment = 25

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
        palette.setColor(QtGui.QPalette.Background, Qt.white)
        self.setPalette(palette)

        # Instantiate the single logger for the UI
        self.logger = Logger()
        # self.logger.enable_console = True
        self.logger.enable_console = False
        self.logger.enable_file = True

        # TODO: Set patient_id from the UI
        self.logger.patient_id = "13c50304-5a34-4a39-8665-bde212f2f206"
        self.logger.path = os.path.join("/tmp", "ovve_logs", self.logger.patient_id)
        self.logger.filename = str(datetime.datetime.now()) + ".log.txt"


        if not is_sim:
            self.comms_handler = CommsLink()
        else:
            self.comms_handler = CommsSimulator()

        self.comms_handler.new_params.connect(self.update_ui_params)
        self.comms_handler.new_alarms.connect(self.update_ui_alarms)
        self.new_settings_signal.connect(self.comms_handler.update_settings)
        self.comms_handler.start()


    def get_mode_display(self, mode):
        return self.settings.mode_switcher.get(mode, "invalid")

    def get_ie_ratio_display(self, ie_ratio):
        return self.settings.ie_ratio_switcher.get(ie_ratio, "invalid")

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

    def update_ui_params(self, params_dict: dict) -> None:
        self.params = Params()
        self.params.from_dict(params_dict)
        self.logger.log("params", self.params.to_JSON())
        self.updateMainDisplays()
        self.updateGraphs()

    def _flash_background_color(self, col: QColor):
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Background, col)
        self.setPalette(palette)

    color = pyqtProperty(QColor, fset=_flash_background_color)

    def update_ui_alarms(self, alarms_dict: dict) -> None:
        self.alarms = Alarms()
        self.alarms.from_dict(alarms_dict)
        self.logger.log("alarms", self.alarms.to_JSON())
        for i in range(len(alarms_dict)):
            if list(alarms_dict.items())[i][1]:
                self.showAlarm(i)
                self.alarm_state = True
                self.alarmBackgroundFlash = QPropertyAnimation(self, b"color")
                self.alarmBackgroundFlash.setDuration(2500)
                self.alarmBackgroundFlash.setLoopCount(-1)
                self.alarmBackgroundFlash.setStartValue(QColor(255,255,255))
                self.alarmBackgroundFlash.setKeyValueAt(0.49, QColor(255, 255, 255))
                self.alarmBackgroundFlash.setKeyValueAt(0.51, QColor(255, 0, 0))
                self.alarmBackgroundFlash.setEndValue(QColor(255,0,0))
                self.alarmBackgroundFlash.start()
        #TODO: Implement UI alarm handling

    def updateMainDisplays(self) -> None:
        self.mode_button_main.updateValue(
            self.get_mode_display(self.settings.mode))
        self.resp_rate_button_main.updateValue(self.settings.resp_rate)
        self.tv_button_main.updateValue(self.settings.tv)
        self.ie_button_main.updateValue(
            self.get_ie_ratio_display(self.settings.ie_ratio))
        self.resp_rate_display_main.updateValue(self.params.resp_rate_meas)
        self.peep_display_main.updateValue(self.params.peep)
        self.tv_insp_display_main.updateValue(self.params.tv_insp)
        self.tv_exp_display_main.updateValue(self.params.tv_exp)
        self.ppeak_display_main.updateValue(self.params.ppeak)
        self.pplat_display_main.updateValue(self.params.pplat)

    def updatePageDisplays(self) -> None:
        self.mode_page_value_label.setText(
            self.get_mode_display(self.settings.mode))
        self.resp_rate_page_value_label.setText(str(self.settings.resp_rate))
        self.tv_page_value_label.setText(str(self.settings.tv))
        self.ie_ratio_page_value_label.setText(
            self.get_ie_ratio_display(self.settings.ie_ratio))
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
    def incrementMode(self) -> None:
        self.local_settings.mode += 1
        if self.local_settings.mode >= len(self.settings.mode_switcher):
            self.local_settings.mode -= len(self.settings.mode_switcher)
        self.mode_page_value_label.setText(
            self.get_mode_display(self.local_settings.mode))

    def decrementMode(self) -> None:
        self.local_settings.mode -= 1
        if self.local_settings.mode < 0:
            self.local_settings.mode += len(self.settings.mode_switcher)
        self.mode_page_value_label.setText(
            self.get_mode_display(self.local_settings.mode))

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

    def incrementIERatio(self) -> None:
        self.local_settings.ie_ratio += 1
        if self.local_settings.ie_ratio >= len(
                self.settings.ie_ratio_switcher):
            self.local_settings.ie_ratio -= len(
                self.settings.ie_ratio_switcher)
        self.ie_ratio_page_value_label.setText(
            self.get_ie_ratio_display(self.local_settings.ie_ratio))

    def decrementIERatio(self) -> None:
        self.local_settings.ie_ratio -= 1
        if self.local_settings.ie_ratio < 0:
            self.local_settings.ie_ratio += len(
                self.settings.ie_ratio_switcher)
        self.ie_ratio_page_value_label.setText(
            self.get_ie_ratio_display(self.local_settings.ie_ratio))

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
            self.showStartStopConfirm()

    def showAlarm(self, code: int):
        d = QDialog()
        d.setFixedWidth(600)
        d.setFixedHeight(300)

        d_h_box_1 = QHBoxLayout()
        d_h_box_2 = QHBoxLayout()
        d_v_box = QVBoxLayout()
        d_label = QLabel(list(self.alarms.to_dict().items())[code][0])
        d_label.setFont(self.ui_settings.page_settings.mainLabelFont)
        d_label.setWordWrap(True)
        d_label.setAlignment(Qt.AlignCenter)

        d_ack = QPushButton("Cancel")
        d_ack.clicked.connect(lambda: self.dismissAlarmPopup(code, d))
        d_ack.setFont(self.ui_settings.simple_button_settings.valueFont)
        d_ack.setStyleSheet("QPushButton {background-color: " +
                               self.ui_settings.page_settings.cancelColor
                               + ";}")

        d_h_box_1.addWidget(d_label)
        d_h_box_2.addWidget(d_ack)
        d_h_box_2.setSpacing(100)
        d_v_box.addLayout(d_h_box_1)
        d_v_box.addLayout(d_h_box_2)

        d.setLayout(d_v_box)
        d.setWindowTitle("Confirm Stop")
        d.setWindowModality(Qt.ApplicationModal)
        d.exec_()

    def dismissAlarmPopup(self, code: int, d: QDialog):
        alarms_dict = self.alarms.to_dict()
        alarms_items = list(alarms_dict.items())
        alarms_dict[alarms_items[code][0]] = False
        print(f'Setting{alarms_items[code][0]} to False')
        self.alarms.from_dict(alarms_dict)
        self.comms_handler.new_alarms
        # print(self.alarms.to_dict())
        d.reject()


    #TODO: Potentially rethink this: it clears all alarms at once so may not work well for simultaneous alarms
    def clearAlarms(self):
        self.alarm_state = False
        self.setStyleSheet("{background-color: white;}")


    def showStartStopConfirm(self):
        d = QDialog()
        d.setFixedWidth(600)
        d.setFixedHeight(300)

        d_h_box_1 = QHBoxLayout()
        d_h_box_2 = QHBoxLayout()
        d_v_box = QVBoxLayout()
        d_label = QLabel("Caution: this will stop ventilation immediately. "
                         "Proceed?")
        d_label.setFont(self.ui_settings.page_settings.mainLabelFont)
        d_label.setWordWrap(True)
        d_label.setAlignment(Qt.AlignCenter)

        d_cancel = QPushButton("Cancel")
        d_cancel.clicked.connect(lambda: d.reject())
        d_cancel.setFont(self.ui_settings.simple_button_settings.valueFont)
        d_cancel.setStyleSheet("QPushButton {background-color: " +
                               self.ui_settings.page_settings.cancelColor
                               + ";}")

        d_confirm = QPushButton("Confirm")
        d_confirm.clicked.connect(lambda: self.stopVentilation(d))
        d_confirm.setFont(self.ui_settings.simple_button_settings.valueFont)
        d_confirm.setStyleSheet("QPushButton {background-color: " +
                               self.ui_settings.page_settings.commitColor
                               + ";}")

        d_h_box_1.addWidget(d_label)
        d_h_box_2.addWidget(d_cancel)
        d_h_box_2.addWidget(d_confirm)
        d_h_box_2.setSpacing(100)
        d_v_box.addLayout(d_h_box_1)
        d_v_box.addLayout(d_h_box_2)

        d.setLayout(d_v_box)
        d.setWindowTitle("Confirm Stop")
        d.setWindowModality(Qt.ApplicationModal)
        d.exec_()

    def stopVentilation(self, d: QDialog):
        d.reject()
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
        self.display(0)
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
        self.display(0)
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
        self.display(0)
        self.passChanges()
        self.local_settings = deepcopy(self.settings)
        self.updatePageDisplays()

    def commitIERatio(self) -> None:
        self.logChange(
            Change(
                datetime.datetime.now(),
                "I/E Ratio",
                self.get_ie_ratio_display(self.settings.ie_ratio),
                self.get_ie_ratio_display(self.local_settings.ie_ratio),
            ))
        self.settings.ie_ratio = self.local_settings.ie_ratio
        self.ie_button_main.updateValue(
            self.get_ie_ratio_display(self.settings.ie_ratio))
        self.display(0)
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
        self.display(0)
        self.passChanges()
        self.updatePageDisplays()
        #TODO: Modify some equivalent of local settings for alarms? Not sure how this works

    def cancelChange(self) -> None:
        self.local_settings = deepcopy(self.settings)
        self.updateMainDisplays()
        self.display(0)
        self.updatePageDisplays()

    def passChanges(self) -> None:
        #self.settings_callback(self.settings)
        settings_str = self.settings.to_JSON()
        self.logger.log("settings,", settings_str)
        j = json.loads(settings_str)
        self.new_settings_signal.emit(j)

    def logChange(self, change: Change) -> None:
        if change.old_val != change.new_val:
            print(change.display())
        # TODO: Actually log the change in some data structure

    def set_settings_callback(
            self, settings_callback: Callable[[Settings], None]) -> None:
        self.settings_callback = settings_callback

    def closeEvent(self, *args, **kwargs):
        self.comms_handler.terminate()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F:
            if self.fullscreen:
                self.hide()
                self.showNormal()
                self.fullscreen = False

            elif not self.fullscreen:
                self.hide()
                self.showFullScreen()
                self.fullscreen = True

        elif event.key() == QtCore.Qt.Key_Q:
            self.close()

        elif event.key() == QtCore.Qt.Key_W:
            self.comms_handler.fireAlarm(0)

        elif event.key() == QtCore.Qt.Key_E:
            self.comms_handler.fireAlarm(1)

        elif event.key() == QtCore.Qt.Key_R:
            self.comms_handler.fireAlarm(2)

        elif event.key() == QtCore.Qt.Key_T:
            self.comms_handler.fireAlarm(3)

        elif event.key() == QtCore.Qt.Key_Y:
            self.comms_handler.fireAlarm(4)

        elif event.key() == QtCore.Qt.Key_U:
            self.comms_handler.fireAlarm(5)

        elif event.key() == QtCore.Qt.Key_I:
            self.comms_handler.fireAlarm(6)


def main() -> None:
    parser = argparse.ArgumentParser(description='User interface for OVVE')
    parser.add_argument('-s', "--sim", action='store_true', 
                        help='Run with simulated data')
    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = MainWindow(args.sim)
    window.showNormal()
    app.exec_()
    sys.exit()


if __name__ == '__main__':
    main()
