"""
Read-only alarms from the MCU
"""
import json
from typing import Union
from copy import deepcopy

class Alarms():
    """
    Params defined in serialpacketv0.26.pptx
    """
    def __init__(self) -> None:
        self._alarms: dict = {
            "power_loss": False,
            "low_battery": False,
            "loss_of_breathing_circuit_integrity": False,
            "high_airway_pressure": False,
            "low_airway_pressure": False,
            "low_delivered_tidal_volume": False,
            "apnea": False,
            "crc_error": False,
            "dropped_packet": False,
            "serial_comm_error": False,
            "packet_version_unsupported": False,
            "mode_value_mismatch": False,
            "respiratory_rate_setpoint_mismatch": False,
            "tidal_volume_value_mismatch": False,
            "ie_ratio_mismatch": False,
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
            if key in self._alarms:
                self._alarms[key] = input_dict[key]
            else:
                print("ALARM WAS SET WITH UNKNOWN KEY! " + key)

    def from_JSON(self, j_str: str) -> None:
        j = json.loads(j_str)
        self.from_dict(j)
