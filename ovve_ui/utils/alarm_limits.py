import typing
from utils.alarm_limit_type import AlarmLimitType

class AlarmLimits:
    def __init__(self):
        pressure_increment = 1
        resp_rate_increment = 1


        self.alarm_limits = {
            AlarmLimitType.HIGH_PRESSURE: {"name": "Upper Pressure Alarm",
                                            "increment": pressure_increment,
                                           "settable": True,
                                           "warning_limit": 40,
                                           "hard_limit": 60,
                                           "low": False,
                                           "pair": AlarmLimitType.LOW_PRESSURE},

            AlarmLimitType.LOW_PRESSURE: {"name": "Lower Pressure Alarm",
                                            "increment": pressure_increment,
                                           "settable": True,
                                           "warning_limit": None,
                                           "hard_limit": 0,
                                            "low": True,
                                           "pair": AlarmLimitType.HIGH_PRESSURE},

            AlarmLimitType.HIGH_VOLUME: {"name": "Upper Volume Alarm",
                                            "increment": None,
                                           "settable": False,
                                           "warning_limit": None,
                                           "hard_limit": None,
                                            "low": False,
                                           "pair": AlarmLimitType.LOW_VOLUME},

            AlarmLimitType.LOW_VOLUME: {"name": "Lower Volume Alarm",
                                            "increment": None,
                                           "settable": False,
                                           "warning_limit": None,
                                           "hard_limit": None,
                                            "low": True,
                                           "pair": AlarmLimitType.HIGH_VOLUME},

            AlarmLimitType.HIGH_RESP_RATE: {"name": "Upper Resp. Rate Alarm",
                                            "increment": resp_rate_increment,
                                           "settable": True,
                                           "warning_limit": None,
                                           "hard_limit": 37,
                                            "low": False,
                                           "pair": AlarmLimitType.LOW_RESP_RATE},

            AlarmLimitType.LOW_RESP_RATE: {"name": "Lower Resp. Rate Alarm",
                                            "increment": resp_rate_increment,
                                           "settable": True,
                                           "warning_limit": None,
                                           "hard_limit": 3,
                                            "low": True,
                                           "pair": AlarmLimitType.HIGH_RESP_RATE},
        }

