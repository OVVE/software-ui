from utils.settings import Settings
import typing
from enum import Enum

class AlarmLimit:
    def __init__(self, name, value, increment = None,
                 settable = True, warning_limit = None, hard_limit = None):
        self.name = name
        self.value = value
        self.increment = increment
        self.settable = settable
        self.warning_limit = warning_limit
        self.hard_limit = hard_limit


class AlarmLimitType(Enum):
    HIGH_PRESSURE = 0
    LOW_PRESSURE = 1
    HIGH_VOLUME = 2
    LOW_VOLUME = 3
    HIGH_RESP_RATE = 4
    LOW_RESP_RATE = 5


class AlarmLimits:
    def __init__(self, window):
        pressure_increment = 1
        resp_rate_increment = 1


        self.alarm_limits = {
            AlarmLimitType.HIGH_PRESSURE: {"name": "Upper Pressure Alarm",
                                           "value": window.settings.high_pressure_limit,
                                            "increment": pressure_increment,
                                           "settable": True,
                                           "warning_limit": 40,
                                           "hard_limit": 60},

            AlarmLimitType.LOW_PRESSURE: {"name": "Lower Pressure Alarm",
                                           "value": window.settings.low_pressure_limit,
                                            "increment": pressure_increment,
                                           "settable": True,
                                           "warning_limit": None,
                                           "hard_limit": 0},

            AlarmLimitType.HIGH_VOLUME: {"name": "Upper Volume Alarm",
                                           "value": window.settings.high_volume_limit,
                                            "increment": None,
                                           "settable": False,
                                           "warning_limit": None,
                                           "hard_limit": None},

            AlarmLimitType.LOW_VOLUME: {"name": "Lower Volume Alarm",
                                           "value": window.settings.low_volume_limit,
                                            "increment": None,
                                           "settable": False,
                                           "warning_limit": None,
                                           "hard_limit": None},

            AlarmLimitType.HIGH_RESP_RATE: {"name": "Upper Resp. Rate Alarm",
                                           "value": window.settings.high_resp_rate_limit,
                                            "increment": resp_rate_increment,
                                           "settable": True,
                                           "warning_limit": None,
                                           "hard_limit": None},

            AlarmLimitType.LOW_RESP_RATE: {"name": "Lower Resp. Rate Alarm",
                                           "value": window.settings.low_resp_rate_limit,
                                            "increment": resp_rate_increment,
                                           "settable": True,
                                           "warning_limit": None,
                                           "hard_limit": 0},
        }

