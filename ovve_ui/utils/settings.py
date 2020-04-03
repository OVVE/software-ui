"""
Settings that are sent to MCU
"""
import json
from typing import List


class Settings():
    def __init__(self) -> None:
        self.run_state: int = 0
        self.mode: int = 0
        self.resp_rate: int = 0
        self.tv: int = 0
        self.ie_ratio: int = 0

        
    def to_JSON(self) -> str:
        j = {}
        j['run_state'] = self.run_state
        j['mode'] = self.mode
        j['tv'] = self.tv
        j['resp_rate'] = self.resp_rate
        j['ie_ratio'] = self.ie_ratio
        return json.dumps(j)

    #TODO: add error handling for bad dict keys
    def from_dict(self, settings_dict: dict) -> None:
        self.run_state = settings_dict['run_state']
        self.mode = settings_dict['mode']
        self.tv = settings_dict['tv']
        self.resp_rate = settings_dict['resp_rate']
        self.ie_ratio = settings_dict['ie_ratio']

    def from_json(self, j_str: str) -> None:
        j = json.loads(j_str)
        self.from_dict(j)
    