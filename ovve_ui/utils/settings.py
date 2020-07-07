"""
Settings that are sent to MCU
"""
import json
from typing import List
from utils.alarm_limit_type import AlarmLimitType


class Settings():
    def __init__(self) -> None:
        self.should_shut_down = 0
        self.run_state: int = 0
        self.mode: int = 0

        self.mode_switcher: dict = {0: 'CMV', 1: 'AC', 2: 'SIMV'}

        self.resp_rate: int = 20
        self.tv: int = 475
        self.ie_ratio_enum: int = 0

        #TODO: Adjust these default values
        self.alarm_limit_values = {
            AlarmLimitType.HIGH_PRESSURE: 40,
            AlarmLimitType.LOW_PRESSURE: -1,
            AlarmLimitType.HIGH_VOLUME: self.tv * 1.2,
            AlarmLimitType.LOW_VOLUME: self.tv * 0.8,
            AlarmLimitType.HIGH_RESP_RATE: 20,
            AlarmLimitType.LOW_RESP_RATE: 0,
        }

        self.silence_time: int = 2  #Number of minutes for which alarm is silenced

        self.ie_ratio_switcher: dict = {
            0: 1.0,
            1: float(1 / 1.5),
            2: float(1 / 2),
            3: float(1 / 3)
        }

    @property
    def high_pressure_limit(self) -> int:
        return self.alarm_limit_values[AlarmLimitType.HIGH_PRESSURE]

    @property
    def low_pressure_limit(self) -> int:
        return self.alarm_limit_values[AlarmLimitType.LOW_PRESSURE]

    @property
    def high_volume_limit(self) -> int:
        return self.alarm_limit_values[AlarmLimitType.HIGH_VOLUME]

    @property
    def low_volume_limit(self) -> int:
        return self.alarm_limit_values[AlarmLimitType.LOW_VOLUME]

    @property
    def high_resp_rate_limit(self) -> int:
        return self.alarm_limit_values[AlarmLimitType.HIGH_RESP_RATE]

    @property
    def low_resp_rate_limit(self) -> int:
        return self.alarm_limit_values[AlarmLimitType.LOW_RESP_RATE]

    def to_JSON(self) -> str:
        j = {}
        j['should_shut_down'] = self.should_shut_down
        j['run_state'] = self.run_state
        j['mode'] = self.mode
        j['tv'] = self.tv
        j['resp_rate'] = self.resp_rate
        j['ie_ratio_enum'] = self.ie_ratio_enum
        j['high_pressure_limit'] = self.alarm_limit_values[
            AlarmLimitType.HIGH_PRESSURE]
        j['low_pressure_limit'] = self.alarm_limit_values[
            AlarmLimitType.LOW_PRESSURE]
        j['high_volume_limit'] = self.alarm_limit_values[
            AlarmLimitType.HIGH_VOLUME]
        j['low_volume_limit'] = self.alarm_limit_values[
            AlarmLimitType.LOW_VOLUME]
        j['high_resp_rate_limit'] = self.alarm_limit_values[
            AlarmLimitType.HIGH_RESP_RATE]
        j['low_resp_rate_limit'] = self.alarm_limit_values[
            AlarmLimitType.LOW_RESP_RATE]
        return json.dumps(j)

    #TODO: add error handling for bad dict keys
    def from_dict(self, settings_dict: dict) -> None:
        self.should_shut_down = settings_dict['should_shut_down']
        self.run_state = settings_dict['run_state']
        self.mode = settings_dict['mode']
        self.tv = settings_dict['tv']
        self.resp_rate = settings_dict['resp_rate']
        self.ie_ratio_enum = settings_dict['ie_ratio_enum']
        self.alarm_limit_values[AlarmLimitType.HIGH_PRESSURE] = settings_dict[
            'high_pressure_limit']
        self.alarm_limit_values[
            AlarmLimitType.LOW_PRESSURE] = settings_dict['low_pressure_limit']
        self.alarm_limit_values[
            AlarmLimitType.HIGH_VOLUME] = settings_dict['high_volume_limit']
        self.alarm_limit_values[
            AlarmLimitType.LOW_VOLUME] = settings_dict['low_volume_limit']
        self.alarm_limit_values[AlarmLimitType.HIGH_RESP_RATE] = settings_dict[
            'high_resp_rate_limit']
        self.alarm_limit_values[AlarmLimitType.LOW_RESP_RATE] = settings_dict[
            'low_resp_rate_limit']

    def from_json(self, j_str: str) -> None:
        j = json.loads(j_str)
        self.from_dict(j)
