"""

"""
import datetime
from typing import Union


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

        # ToDo: For the alarm all the reported alarmcodes will also have to be logged along with 
        # the acknowledgement of the alarm

    def display(self) -> str:
        return f"{self.time}: {self.setting} changed from {self.old_val} to {self.new_val}"
