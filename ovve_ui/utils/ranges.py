 
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


"""
Settings that are sent to MCU
"""
import json
from typing import List
from copy import deepcopy


class Ranges():
    def __init__(self) -> None:
        self._ranges: dict = {
            "min_resp_rate": 5,  #Unit: bpm
            "max_resp_rate": 35,
            "resp_rate_increment": 1,
            "min_tv": 150,  #Unit: mL
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
