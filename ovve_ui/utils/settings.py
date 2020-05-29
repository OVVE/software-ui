"""
Settings that are sent to MCU
"""
import json
from typing import List


class Settings():
    def __init__(self) -> None:
        self.run_state: int = 0
        self.mode: int = 0

        self.mode_switcher: dict = {0: 'NAC', 1: 'AC', 2: 'SIMV'}

        self.resp_rate: int = 20
        self.tv: int = 475
        self.ie_ratio_enum: int = 0

        #TODO: Come up with sensible default values for these, currently completely made up
        self.high_pressure_limit: int = 50
        self.low_pressure_limit: int = 10
        self.high_volume_limit: int = 800
        self.low_volume_limit: int = 0
        self.high_resp_rate_limit: int = 20
        self.low_resp_rate_limit: int = 0

        self.silence_time: int = 2  #Number of minutes for which alarm is silenced

        self.ie_ratio_switcher: dict = {
            0: 1.0,
            1: float(1 / 1.5),
            2: float(1 / 2),
            3: float(1 / 3)
        }

    def to_JSON(self) -> str:
        j = {}
        j['run_state'] = self.run_state
        j['mode'] = self.mode
        j['tv'] = self.tv
        j['resp_rate'] = self.resp_rate
        j['ie_ratio_enum'] = self.ie_ratio_enum
        j['high_pressure_limit'] = self.high_pressure_limit
        j['low_pressure_limit'] = self.low_pressure_limit
        j['high_volume_limit'] = self.high_volume_limit
        j['low_volume_limit'] = self.low_volume_limit
        j['high_resp_rate_limit'] = self.high_resp_rate_limit
        j['low_resp_rate_limit'] = self.low_resp_rate_limit
        return json.dumps(j)

    #TODO: add error handling for bad dict keys
    def from_dict(self, settings_dict: dict) -> None:
        self.run_state = settings_dict['run_state']
        self.mode = settings_dict['mode']
        self.tv = settings_dict['tv']
        self.resp_rate = settings_dict['resp_rate']
        self.ie_ratio_enum = settings_dict['ie_ratio_enum']
        self.high_pressure_limit = settings_dict['high_pressure_limit']
        self.low_pressure_limit = settings_dict['low_pressure_limit']
        self.high_volume_limit = settings_dict['high_volume_limit']
        self.low_volume_limit = settings_dict['low_volume_limit']
        self.high_resp_rate_limit = settings_dict['high_resp_rate_limit']
        self.low_resp_rate_limit = settings_dict['low_resp_rate_limit']

    def from_json(self, j_str: str) -> None:
        j = json.loads(j_str)
        self.from_dict(j)
