"""
Read-only parameters from the MCU
""""
from typing import Union
import json 


class Params():
    def __init__(self) -> None:
        self.peep: int = 0
        self.tv_insp: int = 0
        self.tv_exp: int = 0
        self.ppeak: int = 0
        self.pplat: Union[int, float] = 0

    def set_test_params(self) -> None:
        self.peep = 5
        self.tv_insp = 435
        self.tv_exp = 340
        self.ppeak = 20
        self.pplat = 2.5
        
    def to_JSON(self) -> str:
        j = {}
        j['peep'] = self.peep
        j['tv_insp'] = self.tv_insp
        j['tv_exp'] = self.tv_exp
        j['ppeak'] = self.ppeak
        j['pplat'] = self.pplat
        return json.dumps(j)