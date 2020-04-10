"""
Settings that are sent to MCU
"""
import json
from typing import List
from copy import deepcopy

class Ranges():
    def __init__(self) -> None:
        self._ranges: dict = {
            "min_resp_rate": 5, #Unit: bpm
            "max_resp_rate": 35,
            "resp_rate_increment": 1,
            "min_tv": 150, #Unit: mL
            "max_tv": 800,
            "tv_increment": 25
        }

    def to_JSON(self) -> str:
        """ Convert OVVE UI Params to JSON file """
        return json.dumps(self._alarms)

    def to_dict(self) -> dict:
        """ Make a copy of the alarms dict """
        return deepcopy(self._alarms)

    def from_dict(self, input_dict: dict) -> None:
        """ Set OVVE UI alarms from input dictionary """
        for key in input_dict:
            # Check if key from input_dict exists in ours
            if key in self._ranges:
                self._ranges[key] = input_dict[key]
            else:
                print("RANGE WAS SET WITH UNKNOWN KEY! " + key)

    def from_JSON(self, j_str: str) -> None:
        j = json.loads(j_str)
        self.from_dict(j)
