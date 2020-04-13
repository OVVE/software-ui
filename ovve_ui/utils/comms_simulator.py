import json
import random
import time
from threading import Thread, Lock

from utils.params import Params
from utils.settings import Settings
from utils.alarms import Alarms

from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal


class CommsSimulator(QThread):
    new_params = pyqtSignal(dict)
    new_alarms = pyqtSignal(dict)

    def __init__(self) -> None:
        QThread.__init__(self)
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
        params_str = params.to_JSON()
        params_dict = json.loads(params_str)
        alarms = Alarms()
        alarms_dict = alarms.to_dict()
        alarm_interval = 2
        alarm_to_set = 0

        while not self.done:
            self.settings_lock.acquire()
            if self.settings.run_state > 0:
                params_dict['run_state'] = self.settings.run_state
                params_dict['seq_num'] = self.seqnum
                params_dict['packet_version'] = self.packet_version
                params_dict['mode'] = self.settings.mode
                params_dict['resp_rate_meas'] = self.settings.resp_rate
                params_dict['resp_rate_set'] = self.settings.resp_rate
                params_dict['tv_meas'] = self.settings.tv
                params_dict['tv_set'] = self.settings.tv
                params_dict['ie_ratio_meas'] = self.settings.ie_ratio
                params_dict['ie_ratio_set'] = self.settings.ie_ratio
                params_dict['peep'] = random.randrange(3, 6)
                params_dict['ppeak'] = random.randrange(15, 20)
                params_dict['pplat'] = random.randrange(15, 20)
                params_dict['pressure'] = random.randrange(15, 20)
                params_dict['flow'] = random.randrange(15, 20)
                params_dict['tv_insp'] = random.randrange(475, 575)
                params_dict['tv_exp'] = random.randrange(475, 575)
                params_dict['tv_rate'] = random.randrange(475, 575)
                params_dict['control_state'] = 0
                params_dict['battery_level'] = 255
                self.new_params.emit(params_dict)

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
