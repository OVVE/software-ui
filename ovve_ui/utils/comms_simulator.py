import json
import logging
import random
import time
from threading import Thread, Lock

from utils.params import Params
from utils.settings import Settings
from utils.Alarm import AlarmType
from utils.in_packet import InPacket
from utils.out_packet import OutPacket
from utils.control_state import ControlState

from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from copy import deepcopy

class CommsSimulator(QThread):
    new_params = pyqtSignal(Params)
    new_alarms = pyqtSignal(int)
    lost_comms_signal = pyqtSignal()

    def __init__(self) -> None:
        QThread.__init__(self)
        self.logger = logging.getLogger()
        self.done = False
        self.settings = Settings()
        self.seqnum = 0
        self.packet_version = 1
        self.settings_lock = Lock()
        self.firedAlarms = []
        self.in_pkt = InPacket()
        self.out_pkt = OutPacket()
        self.alarmbits = 0
        self.ackbits = 0
        self.control_state = ControlState.UNCALIBRATED
        self.enable_calibration = False

    def update_settings(self, settings_dict: dict) -> None:
        self.settings_lock.acquire()
        self.settings.from_dict(settings_dict)
        self.settings_lock.release()

    def ready_to_calibrate(self):
        self.logger.debug("CommsSim: ready to calibrate")
        self.enable_calibration = True

    def ready_to_ventilate(self):
        self.logger.debug("CommsSim: ready to ventilate")
        self.enable_calibration = False

    def set_alarm_ackbits(self, ackbits: int) -> None:
        self.logger.debug("CommsSimulator got ackbits " + str(bin(ackbits)))
        self.ackbits = ackbits & self.alarmbits
        self.alarmbits = self.alarmbits &  ~self.ackbits

    def fireAlarm(self, key: int):
        self.firedAlarms.append(key)

    def run(self) -> None:
        params = Params()
        alarmindex = 0
        while not self.done:
            
            # Simulate controller state changes for calibration
            if self.control_state == ControlState.UNCALIBRATED:
                self.logger.debug("CommsSim: ControlState UNCALIBRATED")
                if self.enable_calibration:
                    self.control_state = ControlState.SENSOR_CALIBRATION
                params.control_state = self.control_state
                self.new_params.emit(params)
            elif self.control_state == ControlState.SENSOR_CALIBRATION:
                self.logger.debug("CommsSim: ControlState SENSOR_CALIBRATION")
                self.control_state = ControlState.SENSOR_CALIBRATION_DONE
                params.control_state = self.control_state
                self.new_params.emit(params)
            elif self.control_state == ControlState.SENSOR_CALIBRATION_DONE:
                self.logger.debug("CommsSim: ControlState SENSOR_CALIBRATION_DONE")
                if not self.enable_calibration:
                    self.logger.debug("CommsSim: ControlState IDLE")
                    self.control_state = ControlState.IDLE
                params.control_state = self.control_state
                self.new_params.emit(params)

            else:            
                self.settings_lock.acquire()
                if self.settings.run_state > 0:
                    params.run_state = self.settings.run_state
                    params.control_state = self.control_state
                    params.seq_num = self.seqnum
                    params.packet_version = self.packet_version
                    params.mode = self.settings.mode
                    params.resp_rate_meas = self.settings.resp_rate
                    params.resp_rate_set = self.settings.resp_rate
                    params.tv_meas = random.randrange(0, 1000)
                    params.tv_set = self.settings.tv
                    
                    # Simulate conversion to / from fixed point representation
                    ie_fraction = self.settings.ie_ratio_switcher.get(self.settings.ie_ratio_enum, -1)
                    ie_fixed = self.out_pkt.ie_fraction_to_fixed(ie_fraction)
                    ie_fraction2 = self.in_pkt.ie_fixed_to_fraction(ie_fixed)
                    params.ie_ratio_meas = ie_fraction2
                    params.ie_ratio_set = ie_fraction

                    params.peep = random.uniform(3, 6)
                    params.ppeak = random.uniform(15, 20)
                    params.pplat = random.uniform(15, 20)
                    params.pressure = random.uniform(-40, 40)
                    params.flow = random.uniform(0, 55)
                    params.tv_insp = random.uniform(475, 575)
                    params.tv_exp = random.uniform(475, 575)
                    params.tv_rate = random.uniform(475, 575)
                    params.battery_level = random.randint(0, 100)
                    self.new_params.emit(params)

                    # if (self.seqnum == 9):
                    #     print("Emitting lost comms signal")
                    #     self.lost_comms_signal.emit()

                    if (self.seqnum % 100 == 99):
                        #alarmindex = random.randrange(len(list(AlarmType)))
                        alarmindex += 1
                        alarmtype = list(AlarmType)[alarmindex]
                        self.alarmbits |= 1 << alarmtype.value
                        # if random.randint(0,3) == 0:
                        #     alarmindex2 = random.randrange(len(list(AlarmType)))
                        #     alarmtype2 = list(AlarmType)[alarmindex2]
                        #     self.alarmbits |= 1 << alarmtype2.value
                        #     self.logger.debug("Emitting two alarms " + alarmtype.name + ", " + alarmtype2.name + " bits: " + str(bin(self.alarmbits)))
                        # else:
                        #     self.logger.debug("Emitting an alarm " + alarmtype.name + " bits: " + str(bin(self.alarmbits)))

                        self.new_alarms.emit(self.alarmbits)

                    self.seqnum += 1
                self.settings_lock.release()
            self.msleep(100)
