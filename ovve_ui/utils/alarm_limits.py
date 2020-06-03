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
    HIGH_VOLUME  = 2
    LOW_VOLUME = 3
    HIGH_RESP_RATE = 4
    LOW_RESP_RATE = 5


class AlarmLimits:
    def __init__(self, window):
        pressure_increment = 1
        resp_rate_increment = 1

        self.alarm_limits = {
            AlarmLimitType.HIGH_PRESSURE: AlarmLimit("Upper Pressure Alarm",
                                                     window.settings.high_pressure_limit,
                                                     increment= pressure_increment,
                                                     warning_limit=40,
                                                     hard_limit = 60),

            AlarmLimitType.LOW_PRESSURE: AlarmLimit("Lower Pressure Alarm",
                                                     window.settings.low_pressure_limit,
                                                     increment= pressure_increment,
                                                     hard_limit=0),

            AlarmLimitType.HIGH_VOLUME: AlarmLimit("Upper Volume Alarm",
                                                   window.settings.high_volume_limit,
                                                   settable=False),

            AlarmLimitType.LOW_VOLUME: AlarmLimit("Lower Volume Alarm",
                                                    window.settings.low_volume_limit,
                                                    settable=False),

            AlarmLimitType.HIGH_RESP_RATE: AlarmLimit("Upper Resp. Rate Alarm",
                                                   window.settings.high_resp_rate_limit,
                                                   increment = resp_rate_increment),

            AlarmLimitType.LOW_RESP_RATE: AlarmLimit("Lower Resp. Rate Alarm",
                                                  window.settings.low_resp_rate_limit,
                                                  increment= resp_rate_increment,
                                                  hard_limit= 0)
        }

