"""
Settings that are sent to MCU
"""
import json
from typing import List


class Settings():
    def __init__(self) -> None:
        self.run_state: int = 0
        self.mode: int = 0

        self.mode_switcher: dict = {
            0: 'NAC',
            1: 'AC',
            2: 'SIMV'
        }

        self.resp_rate: int = 20
        self.tv: int = 475
        self.ie_ratio: int = 0

        self.silence_time: int = 1 #Number of minutes for which alarm is silenced

        self.ie_ratio_switcher: dict = {
            0: "1:1",
            1: "1:1.5",
            2: "1:2",
            3: "1:3",
        }
        # False -> Off, True -> On
        # Alarm mode changes from serial comms input
        self.alarm_mode = False

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

    def alarm_code(self):
        # Available alarm codes 0-31
        alarmcodes = [[0, "Power loss (from ECU)"],
                      [1, "Low battery (from ECU)"],
                      [2, "Loss of breathing circuit integrity (from ECU)"],
                      [3, "High airway pressure (from ECU)"],
                      [4, "Low airway pressure (from ECU)"],
                      [5, "Low delivered Tidal Volume (from ECU)"],
                      [6, "Apnea (from ECU)"],
                      [16, "CRC Error (from processor)"],
                      [17, "Dropped packet (from processor)"],
                      [18, "Serial comm Error (from processor)"],
                      [19, "Packet version unsupported (from processor)"],
                      [24, "Mode value mismatch (from UI-CU)"],
                      [25, "Respiratory rate setpoint mismatch (from UI-CU)"],
                      [26, "Tidal volume mismatch (from UI-CU)"],
                      [27, "I/E ratio mismatch"]]

    def get_alarm_display(self):
        if self.alarm_mode:
            return "Alarm ON"
        else:
            return "Alarm OFF"
