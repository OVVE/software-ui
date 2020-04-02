"""

"""
from typing import Union
import datetime

class Change():
    def __init__(self,
                 time: datetime.datetime,
                 setting: str,
                 old_val: Union[int, float],
                 new_val: Union[int, float]) -> None:
        self.time = time
        self.setting = setting
        self.old_val = old_val
        self.new_val = new_val

    def display(self) -> str:
        return f"{self.time}: {self.setting} changed from {self.old_val} to {self.new_val}"