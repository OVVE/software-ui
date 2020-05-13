import json
import random
import time
from threading import Thread, Lock

from utils.params import Params
from utils.settings import Settings
from utils.alarms import Alarms
from utils.in_packet import InPacket
from utils.out_packet import OutPacket

from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from copy import deepcopy

class CommsSimulator(QThread):
    new_params = pyqtSignal(Params)
    new_alarms = pyqtSignal(dict)

    def __init__(self) -> None:
        QThread.__init__(self)
        self.done = False
        self.settings = Settings()
        self.seqnum = 0
        self.packet_version = 1
        self.settings_lock = Lock()
        self.firedAlarms = []
        self.in_pkt = InPacket()
        self.out_pkt = OutPacket()

    def update_settings(self, settings_dict: dict) -> None:
        self.settings_lock.acquire()
        self.settings.from_dict(settings_dict)
        self.settings_lock.release()

    def fireAlarm(self, key: int):
        self.firedAlarms.append(key)

    def run(self) -> None:
        params = Params()
        alarms = Alarms()
        alarms_dict = alarms.to_dict()
        alarm_interval = 2
        alarm_to_set = 0

        while not self.done:
            self.settings_lock.acquire()
            if self.settings.run_state > 0:
                params.run_state = self.settings.run_state
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
                params.control_state = 0
                params.battery_level = random.randint(0, 100)
                self.new_params.emit(params)

                # Every N loops fire an alarm
                # Every time the alarm fires, iterate the alarm that's set to True
                # All other alarms will be false
                # if alarm_interval > 0 and self.seqnum % alarm_interval == 0:
                #     alarms_items = list(alarms_dict.items())
                #     for i in range(0, len(alarms_items)):
                #         if i == alarm_to_set:
                #             alarms_dict[alarms_items[i][0]] = True
                #         else:
                #             alarms_dict[alarms_items[i][0]] = False
                #     self.new_alarms.emit(alarms_dict)
                #     alarm_to_set = (alarm_to_set + 1) % len(alarms_dict.keys())
                #
                alarms_items = list(alarms_dict.items())
                orig_alarms_dict = alarms_dict.copy()

                for i in self.firedAlarms:
                    alarms_dict[alarms_items[i][0]] = True
                self.firedAlarms.clear()
                self.new_alarms.emit(alarms_dict)
                alarms_dict = orig_alarms_dict
                self.seqnum += 1

            self.settings_lock.release()
            self.msleep(100)
