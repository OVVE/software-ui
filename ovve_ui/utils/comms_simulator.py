import json
import random
import time
from threading import Thread, Lock

from utils.params import Params
from utils.settings import Settings
from utils.alarms import Alarms
from utils.logger import Logger

from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal


class CommsSimulator(QThread):
    new_params = pyqtSignal(Params)
    new_alarms = pyqtSignal(dict)

    def __init__(self, logger: Logger) -> None:
        QThread.__init__(self)
        self.logger = logger
        self.done = False
        self.settings = Settings()
        self.seqnum = 0
        self.packet_version = 1
        self.settings_lock = Lock()

    def update_settings(self, settings_dict: dict) -> None:
        self.settings_lock.acquire()
        self.settings.from_dict(settings_dict)
        self.settings_lock.release()

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
                params.tv_meas = self.settings.tv
                params.tv_set = self.settings.tv
                params.ie_ratio_meas = self.settings.ie_ratio
                params.ie_ratio_set = self.settings.ie_ratio
                params.peep = random.randrange(3, 6)
                params.ppeak = random.randrange(15, 20)
                params.pplat = random.randrange(15, 20)
                params.pressure = random.randrange(15, 20)
                params.flow = random.randrange(15, 20)
                params.tv_insp = random.randrange(475, 575)
                params.tv_exp = random.randrange(475, 575)
                params.tv_rate = random.randrange(475, 575)
                params.control_state = 0
                params.battery_level = 255
                self.new_params.emit(params)

                # Every N loops fire an alarm
                # Every time the alarm fires, iterate the alarm that's set to True
                # All other alarms will be false
                if alarm_interval > 0 and self.seqnum % alarm_interval == 0:                      
                    alarms_items = list(alarms_dict.items())
                    for i in range(0, len(alarms_items)):
                        if i == alarm_to_set:
                            alarms_dict[alarms_items[i][0]] = True
                        else:
                            alarms_dict[alarms_items[i][0]] = False
                    self.new_alarms.emit(alarms_dict)
                    alarm_to_set = (alarm_to_set + 1) % len(alarms_dict.keys())
                    
                self.seqnum += 1
            self.settings_lock.release()
            self.sleep(1)
