 
# Copyright 2020 LifeMech  Inc
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, 
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
# is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


import typing
from utils.alarm_limit_type import AlarmLimitType, AlarmLimitPair


class AlarmLimits:
    def __init__(self):
        pressure_increment = 1
        resp_rate_increment = 1

        self.alarm_limit_pairs = {
            AlarmLimitPair.PRESSURE: {
                "short_name": "Pressure",
                "full_name": "Pressure Alarm Setpoint",
                "low": AlarmLimitType.LOW_PRESSURE,
                "high": AlarmLimitType.HIGH_PRESSURE
            },
            AlarmLimitPair.VOLUME: {
                "short_name": "Volume",
                "full_name": "Volume Alarm Setpoint",
                "low": AlarmLimitType.LOW_VOLUME,
                "high": AlarmLimitType.HIGH_VOLUME
            },
            AlarmLimitPair.RESP_RATE: {
                "short_name": "Resp. Rate",
                "full_name": "Resp. Rate Alarm Setpoint",
                "low": AlarmLimitType.LOW_RESP_RATE,
                "high": AlarmLimitType.HIGH_RESP_RATE
            },
        }

        self.alarm_limits = {
            AlarmLimitType.HIGH_PRESSURE: {
                "name": "Upper Pressure Alarm",
                "increment": pressure_increment,
                "settable": True,
                "warning_limit": 40,
                "warning_msg": "You have set a pressure limit above 40 cmH2O",
                "hard_limit": 60,
                "low": False,
                "pair": AlarmLimitType.LOW_PRESSURE
            },
            AlarmLimitType.LOW_PRESSURE: {
                "name": "Lower Pressure Alarm",
                "increment": pressure_increment,
                "settable": True,
                "warning_limit": None,
                "warning_msg": None,
                "hard_limit": None,
                "low": True,
                "pair": AlarmLimitType.HIGH_PRESSURE
            },
            AlarmLimitType.HIGH_VOLUME: {
                "name": "Upper Volume Alarm",
                "increment": None,
                "settable": False,
                "warning_limit": None,
                "warning_msg": None,
                "hard_limit": None,
                "low": False,
                "pair": AlarmLimitType.LOW_VOLUME
            },
            AlarmLimitType.LOW_VOLUME: {
                "name": "Lower Volume Alarm",
                "increment": None,
                "settable": False,
                "warning_limit": None,
                "warning_msg": None,
                "hard_limit": None,
                "low": True,
                "pair": AlarmLimitType.HIGH_VOLUME
            },
            AlarmLimitType.HIGH_RESP_RATE: {
                "name": "Upper Resp. Rate Alarm",
                "increment": resp_rate_increment,
                "settable": True,
                "warning_limit": None,
                "warning_msg": None,
                "hard_limit": 37,
                "low": False,
                "pair": AlarmLimitType.LOW_RESP_RATE
            },
            AlarmLimitType.LOW_RESP_RATE: {
                "name": "Lower Resp. Rate Alarm",
                "increment": resp_rate_increment,
                "settable": True,
                "warning_limit": None,
                "warning_msg": None,
                "hard_limit": 3,
                "low": True,
                "pair": AlarmLimitType.HIGH_RESP_RATE
            },
        }
