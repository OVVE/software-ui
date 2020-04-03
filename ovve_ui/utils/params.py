"""
Read-only parameters from the MCU
"""
import json
from typing import Union


# Params defined in serialpacketv0.26.pptx
class Params():
    def __init__(self) -> None:
        self.seq_num: int = 0
        self.packet_version: int = 0
        self.mode: int = 0
        self.resp_rate_meas: int = 0
        self.resp_rate_set: int = 0
        self.tv_meas: int = 0
        self.tv_set: int = 0
        self.ie_ratio_meas: int = 0
        self.ie_ratio_set: int = 0
        self.peep: int = 0
        self.ppeak: int = 0
        self.pplat: Union[int, float] = 0
        self.pressure: Union[int, float] = 0
        self.flow: Union[int, float] = 0
        self.tv_insp: int = 0
        self.tv_exp: int = 0
        self.tv_min: int = 0 
        self.control_state: int = 0
        self.battery_level: int = 0
        #TODO: handle alarms

   
    def to_JSON(self) -> str:
        j = {}
        j['seq_num'] = self.seq_num
        j['packet_version'] = self.packet_version
        j['mode'] = self.mode
        j['resp_rate_meas'] = self.resp_rate_meas
        j['resp_rate_set'] = self.resp_rate_set
        j['tv_meas'] = self.tv_meas
        j['tv_set'] = self.tv_set
        j['ie_ratio_meas'] = self.ie_ratio_meas
        j['ie_ratio_set'] = self.ie_ratio_set
        j['peep'] = self.peep
        j['ppeak'] = self.ppeak
        j['pplat'] = self.pplat
        j['pressure'] = self.pressure
        j['flow'] = self.flow
        j['tv_insp'] = self.tv_insp
        j['tv_exp'] = self.tv_exp
        j['tv_min'] = self.tv_min 
        j['control_state'] = self.control_state
        j['battery_level'] = self.battery_level
        return json.dumps(j)

    #TODO: add error handling for bad dict keys
    def from_dict(self, j: dict) -> None:
        self.seq_num = j['seq_num']
        self.packet_version = j['packet_version']
        self.mode = j['mode']
        self.resp_rate_meas = j['resp_rate_meas']
        self.resp_rate_set = j['resp_rate_set']
        self.tv_meas = j['tv_meas']
        self.tv_set = j['tv_set']
        self.ie_ratio_meas = j['ie_ratio_meas']
        self.ie_ratio_set = j['ie_ratio_set']
        self.peep = j['peep']
        self.ppeak = j['ppeak']
        self.pplat = j['pplat']
        self.pressure = j['pressure']
        self.flow = j['flow']
        self.tv_insp = j['tv_insp']
        self.tv_exp = j['tv_exp']
        self.tv_min = j['tv_min'] 
        self.control_state = j['control_state']
        self.battery_level = j['battery_level']

    def from_JSON(self, j_str: str) -> None:
        j = json.loads(j_str)
        self.from_dict(j)

