import argparse
import datetime
import json
import logging
import os
import sys
import time
from timeit import default_timer as timer

import uuid
from copy import deepcopy
from logging.handlers import TimedRotatingFileHandler
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

from display.button import FancyDisplayButton, SimpleDisplayButton, PicButton
from display.rectangle import DisplayRect
from display.ui_settings import (DisplayRectSettings, FancyButtonSettings,
                                 SimpleButtonSettings, TextSetting, UISettings)
from typing import Callable
from display.widgets import (initializeHomeScreenWidget, initializeModeWidget,
                             initializeRespiratoryRateWidget,
                             initializeTidalVolumeWidget,
                             initializeIERatioWidget, initializeAlarmWidget,
                             initializeGraphWidget, initializeSettingsWidget,
                             initializeConfirmStopWidget, initializeChangePatientWidget)
from utils.params import Params
from utils.settings import Settings
from utils.alarms import Alarms
from utils.Alarm import Alarm, AlarmHandler
from utils.comms_simulator import CommsSimulator
from utils.comms_link import CommsLink
from utils.ranges import Ranges


class MainWindow(QWidget):
    new_settings_signal = pyqtSignal(dict)

    def __init__(self,
                 port: str,
                 is_sim: bool = False,
                 windowed: bool = False,
                 dev_mode: bool = False) -> None:
        super().__init__()
        self.settings = Settings()
        self.local_settings = Settings()  # local settings are changed with UI
        self.params = Params()
        self.ranges = Ranges()
        self.windowed = windowed
        self.dev_mode = dev_mode
        self.last_main_update_time = 0
        self.main_update_interval = 1.0

        self.patient_id = uuid.uuid4()
        self.patient_id_display = 1
        self.new_patient_id_display =1
        self.logpath = os.path.join("/tmp", "ovve_logs", str(self.patient_id))

        self.battery_img = "battery_grey_full"

        # you can pass new settings for different object classes here
        self.ui_settings = UISettings()
        self.ptr = 0

        self.dateTime = QDateTime.currentDateTime()

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
            "7": QWidget(),
            "8": QWidget(),
            "9": QWidget(),
        }
        self.alarms = Alarms()
        self.shownAlarmCode = None



        self.initalizeAndAddStackWidgets()

        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, Qt.white)
        self.setPalette(palette)


        # Create all directories in the log path
        if not os.path.exists(self.logpath):
            os.makedirs(self.logpath)

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        self.logfileroot = os.path.join(self.logpath, str(self.patient_id) + ".log")

        # The TimedRotatingFileHandler will write a new file each hour
        # After two weeks, the oldest logs will start being deleted
        fh = TimedRotatingFileHandler(self.logfileroot,
                                      when='H',
                                      interval=1,
                                      backupCount=336)

        # Set the filehandler to log raw packets, warnings, and higher
        # Raw packets are logged at custom log level 25, just above INFO
        fh.setLevel(25)

        # Log to console with human-readable output
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)

        # TODO: Create a custom handler for Ignition

        # create formatter and add it to the handlers
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # add the handlers to the logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        if not is_sim:
            self.comms_handler = CommsLink(port)
        else:
            self.comms_handler = CommsSimulator()

        self.comms_handler.new_params.connect(self.update_ui_params)
        self.comms_handler.new_alarms.connect(self.update_ui_alarms)
        self.new_settings_signal.connect(self.comms_handler.update_settings)
        self.comms_handler.start()

        self.alarm_handler = AlarmHandler()
        self.comms_handler.new_alarms.connect(self.alarm_handler.setActiveBits)
        self.alarm_handler.acknowledge_alarm_signal.connect(self.comms_handler.)

    def get_mode_display(self, mode):
        return self.settings.mode_switcher.get(mode, "invalid")

    def ie_fractional_to_ratio_str(self, fractional_ie: float) -> str:
        if fractional_ie <= 0:
            return "invalid"
        elif fractional_ie > 1.0:
            return str(str(fractional_ie) + ":1")
        else:
            d = 1 / fractional_ie
            r = round(d)
            # If close to an integer, round to that integer
            if (abs(d - r) < 0.1):
                return str("1:" + str(r))
            # Otherwise, round to one decimal place
            return str("1:" + str(round(d, 1)))


    def get_ie_ratio_display(self, ie_ratio_enum: int) -> str:
        fractional_ie = self.settings.ie_ratio_switcher.get(ie_ratio_enum, -1)
        return self.ie_fractional_to_ratio_str(fractional_ie)

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

    def makePicButton(self, filename: str, size: Optional[Tuple[int, int]] = None) -> PicButton:
        return PicButton(filename, size = size)

    def makeDisplayRect(
            self,
            label: str,
            value: Union[int, float, str],
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
        initializeSettingsWidget(self)
        initializeConfirmStopWidget(self)
        initializeChangePatientWidget(self)

        for i in self.page:
            self.stack.addWidget(self.page[i])

    def display(self, i) -> None:
        self.stack.setCurrentIndex(i)

    def update_ui_params(self, params: Params) -> None:
        self.params = params
        if self.params.run_state > 0:


            self.logger.info(self.params.to_JSON())
            self.update_ui_alarms()
            self.updateMainDisplays()
            self.updateGraphs()

    def update_ui_alarms(self) -> None:
        while self.alarm_handler.alarms_pending() > 0:
            self.shown_alarm = self.handler.get_highest_priority_alarm()
            self.showAlarm()

    def showAlarm(self) -> None:
        self.alarm_display_label.setText(self.highest_alarm.get_message())
        self.display(5)

    def silenceAlarm(self) -> None:
        self.alarm_handler.acknowledge_alarm(self.highest_alarm)
        self.shown_alarm = None
        self.update_ui_alarms()
        self.display(0)

    def updateMainDisplays(self) -> None:
        t_now = time.time()
        if (t_now - self.last_main_update_time) > self.main_update_interval:
            self.last_main_update_time = t_now
            self.mode_button_main.updateValue(
                self.get_mode_display(self.params.mode))
            self.resp_rate_button_main.updateValue(self.params.resp_rate_set)
            self.tv_button_main.updateValue(self.params.tv_set)
            self.ie_button_main.updateValue(
                self.ie_fractional_to_ratio_str(self.params.ie_ratio_set))
            self.resp_rate_display_main.updateValue(round(self.params.resp_rate_meas, 2))
            self.peep_display_main.updateValue(round(self.params.peep, 1))
            self.tv_insp_display_main.updateValue(round(self.params.tv_insp))
            # self.tv_exp_display_main.updateValue(self.params.tv_exp)
            self.ppeak_display_main.updateValue(round(self.params.ppeak, 1))
            self.pplat_display_main.updateValue(round(self.params.pplat, 1))
            self.main_battery_level_label.setText(f"{self.params.battery_level}%")

            if self.params.battery_level == 0:
                self.battery_img = "battery_grey_0"
            elif self.params.battery_level<=25:
                self.battery_img = "battery_grey_25"
            elif self.params.battery_level<=50:
                self.battery_img = "battery_grey_50"

            elif self.params.battery_level<=75:
                self.battery_img = "battery_grey_75"

            elif self.params.battery_level<=75:
                self.battery_img = "battery_grey_75"

            else:
                self.battery_img = "battery_grey_full"

            self.main_battery_icon.updateValue(os.path.abspath(os.path.join(
                os.path.dirname(__file__),
                f"display/images/batteries/light_theme/{self.battery_img}")))

            #TODO: Get battery level converted to percentage

    def updatePageDisplays(self) -> None:
        self.mode_page_value_label.setText(
            self.get_mode_display(self.settings.mode))
        self.resp_rate_page_value_label.setText(str(self.settings.resp_rate))
        self.tv_page_value_label.setText(str(self.settings.tv))
        self.ie_ratio_page_value_label.setText(
            self.get_ie_ratio_display(self.settings.ie_ratio_enum))

    # TODO: Polish up and process data properly
    def updateGraphs(self) -> None:

        self.pressure_data[self.graph_ptr] = self.params.pressure
        self.pressure_graph_line.setData(self.pressure_data[:self.graph_ptr + 1])
        self.pressure_graph_cache_line.setData(self.pressure_data[self.graph_ptr + 2:])
        self.pressure_graph_cache_line.setPos(self.graph_ptr + 2, 0)
        self.pressure_graph_line.show()

        QtGui.QApplication.processEvents()

        self.flow_data[self.graph_ptr] = self.params.flow
        self.flow_graph_line.setData(self.flow_data[:self.graph_ptr + 1])
        self.flow_graph_cache_line.setData(self.flow_data[self.graph_ptr + 2:])
        self.flow_graph_cache_line.setPos(self.graph_ptr + 2, 0)
        self.flow_graph_line.show()

        QtGui.QApplication.processEvents()

        self.volume_data[self.graph_ptr] = self.params.tv_meas
        self.volume_graph_line.setData(self.volume_data[:self.graph_ptr + 1])
        self.volume_graph_cache_line.setData(self.volume_data[self.graph_ptr + 2:])
        self.volume_graph_cache_line.setPos(self.graph_ptr+2, 0)
        self.volume_graph_line.show()

        QtGui.QApplication.processEvents()

        self.graph_ptr = (self.graph_ptr + 1) % self.graph_width

        if self.graph_ptr == 0:
            self.flow_graph_cache_line.setData(self.flow_data)
            self.flow_graph_cache_line.setPos(0, 0)
            self.flow_graph_cache_line.show()
            self.flow_graph_line.setData(np.empty(0,))

            QtGui.QApplication.processEvents()

            self.pressure_graph_cache_line.setData(self.pressure_data)
            self.pressure_graph_cache_line.setPos(0, 0)
            self.pressure_graph_cache_line.show()
            self.pressure_graph_line.setData(np.empty(0, ))

            QtGui.QApplication.processEvents()

            self.volume_graph_cache_line.setData(self.volume_data)
            self.volume_graph_cache_line.setPos(0, 0)
            self.volume_graph_cache_line.show()
            self.volume_graph_line.setData(np.empty(0, ))

            QtGui.QApplication.processEvents()

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
        self.local_settings.resp_rate += self.ranges._ranges[
            "resp_rate_increment"]
        self.resp_rate_page_value_label.setText(
            str(self.local_settings.resp_rate))
        if self.local_settings.resp_rate + self.ranges._ranges["resp_rate_increment"] \
            > self.ranges._ranges["max_resp_rate"]:
            self.resp_rate_increment_button.hide()
        self.resp_rate_decrement_button.show()

    def decrementRespRate(self) -> None:
        self.local_settings.resp_rate -= self.ranges._ranges[
            "resp_rate_increment"]
        self.resp_rate_page_value_label.setText(
            str(self.local_settings.resp_rate))
        if self.local_settings.resp_rate - self.ranges._ranges["resp_rate_increment"] \
            < self.ranges._ranges["min_resp_rate"]:
            self.resp_rate_decrement_button.hide()
        self.resp_rate_increment_button.show()

    def incrementTidalVol(self) -> None:
        self.local_settings.tv += self.ranges._ranges["tv_increment"]
        self.tv_page_value_label.setText(str(self.local_settings.tv))
        if self.local_settings.tv + self.ranges._ranges["tv_increment"] \
            > self.ranges._ranges["max_tv"]:
            self.tv_increment_button.hide()
        self.tv_decrement_button.show()

    def decrementTidalVol(self) -> None:
        self.local_settings.tv -= self.ranges._ranges["tv_increment"]
        self.tv_page_value_label.setText(str(self.local_settings.tv))
        if self.local_settings.tv - self.ranges._ranges["tv_increment"] \
            < self.ranges._ranges["min_tv"]:
            self.tv_decrement_button.hide()
        self.tv_increment_button.show()

    def incrementIERatio(self) -> None:
        self.local_settings.ie_ratio_enum += 1
        if self.local_settings.ie_ratio_enum >= len(
                self.settings.ie_ratio_switcher):
            self.local_settings.ie_ratio_enum -= len(
                self.settings.ie_ratio_switcher)
        self.ie_ratio_page_value_label.setText(
            self.get_ie_ratio_display(self.local_settings.ie_ratio_enum))

    def decrementIERatio(self) -> None:
        self.local_settings.ie_ratio_enum -= 1
        if self.local_settings.ie_ratio_enum < 0:
            self.local_settings.ie_ratio_enum += len(
                self.settings.ie_ratio_switcher)
        self.ie_ratio_page_value_label.setText(
            self.get_ie_ratio_display(self.local_settings.ie_ratio_enum))

    def changeAlarm(self, new_val) -> None:
        self.local_settings.alarm_mode = new_val

    def changeStartStop(self) -> None:
        if self.settings.run_state == 0:
            self.settings.run_state = 1
            self.start_stop_button_main.updateValue("STOP")
            self.start_stop_button_main.button_settings = SimpleButtonSettings(
                fillColor="#ff0000")
            self.passChanges()

        elif self.settings.run_state == 1:
            self.confirmStop()

    def generateNewPatientID(self) -> None:
        self.new_patient_id = uuid.uuid4()
        self.new_patient_id_display += 1
        self.patient_page_label.setText( f"Current Patient: Patient {self.new_patient_id_display}")
        self.patient_page_label.update()
        # self.generate_new_patient_id_page_button.hide()

    def confirmStop(self) -> None:
        self.display(7)

    def stopVentilation(self) -> None:
        self.settings.run_state = 0
        self.start_stop_button_main.updateValue("START")
        self.start_stop_button_main.button_settings = SimpleButtonSettings()
        self.passChanges()
        self.display(0)

    def commitMode(self) -> None:
        self.settings.mode = self.local_settings.mode
        self.mode_button_main.updateValue(
            self.get_mode_display(self.settings.mode))
        self.display(0)
        self.passChanges()
        self.updatePageDisplays()

    def commitRespRate(self) -> None:
        self.settings.resp_rate = self.local_settings.resp_rate
        self.resp_rate_button_main.updateValue(self.settings.resp_rate)
        self.display(0)
        self.passChanges()
        self.local_settings = deepcopy(self.settings)
        self.updatePageDisplays()

    def commitTidalVol(self) -> None:
        self.settings.tv = self.local_settings.tv
        self.tv_button_main.updateValue(self.settings.tv)
        self.display(0)
        self.passChanges()
        self.local_settings = deepcopy(self.settings)
        self.updatePageDisplays()

    def commitIERatio(self) -> None:
        self.settings.ie_ratio_enum = self.local_settings.ie_ratio_enum
        self.ie_button_main.updateValue(
            self.get_ie_ratio_display(self.settings.ie_ratio_enum))
        self.display(0)
        self.passChanges()
        self.local_settings = deepcopy(self.settings)
        self.updatePageDisplays()

    def commitAlarm(self) -> None:
        self.settings.alarm_mode = self.local_settings.alarm_mode
        self.alarm_button_main.updateValue(self.settings.get_alarm_display())
        self.display(0)
        self.passChanges()
        self.updatePageDisplays()

    def commitNewPatientID(self) -> None:
        print(f"Old patient ID {self.patient_id}")
        self.patient_id = self.new_patient_id
        print(f"New patient ID {self.patient_id}")
        self.new_patient_id = None
        self.patient_id_display = self.new_patient_id_display
        self.new_patient_id_display = self.patient_id_display
        self.settings_patient_label.setText( f"Current Patient: Patient {self.patient_id_display}")
        self.main_patient_label.setText( f"Current Patient: Patient {self.patient_id_display}")


        self.generate_new_patient_id_page_button.show()
        self.display(6)

    def cancelNewPatientID(self) -> None:
        self.new_patient_id = None
        self.new_patient_id_display = None
        self.patient_page_label.setText( f"Current Patient: Patient {self.patient_id_display}")
        self.generate_new_patient_id_page_button.show()
        self.display(6)

    def cancelChange(self) -> None:
        self.local_settings = deepcopy(self.settings)
        self.updateMainDisplays()
        self.display(0)
        self.updatePageDisplays()

    def passChanges(self) -> None:
        #self.settings_callback(self.settings)
        settings_str = self.settings.to_JSON()
        self.logger.info(settings_str)
        j = json.loads(settings_str)
        self.new_settings_signal.emit(j)

    def set_settings_callback(
            self, settings_callback: Callable[[Settings], None]) -> None:
        self.settings_callback = settings_callback

    def closeEvent(self, *args, **kwargs) -> None:
        self.comms_handler.terminate()

    def keyPressEvent(self, event):
        if self.dev_mode:
            if event.key() == QtCore.Qt.Key_F:
                self.windowed = not self.windowed

                if self.windowed:
                    self.hide()
                    self.showNormal()

                else:
                    self.hide()
                    self.showFullScreen()

            if event.key() == QtCore.Qt.Key_Q:
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
    parser.add_argument('-s',
                        "--sim",
                        action='store_true',
                        help='Run with simulated data')

    parser.add_argument('-w',
                        "--windowed",
                        action='store_true',
                        help='Run in windowed mode (fullscreen default)')

    parser.add_argument(
        '-d',
        "--dev_mode",
        action='store_true',
        help=
        'Run in developer mode (alarm hotkeys enabled (w,e,r, etc.) , toggle fullscreen (f) enabled)'
    )

    parser.add_argument('-p',
                        "--port",
                        default='/dev/ttyUSB0',
                        help='Serial port for communication with MCU')
    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = MainWindow(args.port, args.sim, args.windowed, args.dev_mode)
    if window.windowed:
        window.showNormal()
    else:
        window.showFullScreen()
    app.exec_()
    sys.exit()


if __name__ == '__main__':
    main()
