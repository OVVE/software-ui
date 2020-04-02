"""
Settings that are sent to MCU
"""
from typing import List
import json


class Settings:
    def __init__(self):
        self.ac_mode: bool = False  # mode = True -> AC, mode = False -> SIMV
        self.minute_volume: int = 0
        self.resp_rate: int = 0
        self.resp_rate_increment: int = 0
        self.minute_volume_increment: int = 0

        # TODO: validate this assumption
        # ie ratio is an enumeration of possible ie ratios
        # ie ratio id is passed from the MCU as an index into the enumeration
        self.ie_ratio_display: List[str] = ["1:1", "1:1.5", "1:2", "1:3"]
        self.ie_ratio_id: int = 0

    def set_test_settings(self):
        self.ac_mode = False
        self.minute_volume = 10
        self.resp_rate = 14
        self.ie_ratio_id = 0
        self.resp_rate_increment = 1
        self.minute_volume_increment = 1

    def get_ie_display(self) -> str:
        if self.ie_ratio_id < len(self.ie_ratio_display):
            return self.ie_ratio_display[self.ie_ratio_id]

        return "ERROR"

    def get_mode_display(self) -> str:
        if self.ac_mode:
            return "AC"

        return "SIMV"

    def to_JSON(self) -> str:
        j = {}
        j['ac_mode'] = self.ac_mode
        j['minute_volume'] = self.minute_volume
        j['resp_rate'] = self.resp_rate
        j['ie_ratio_id'] = self.ie_ratio_id
        return json.dumps(j)
