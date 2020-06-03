from enum import Enum

class AlarmLimitType(Enum):
    HIGH_PRESSURE = 0
    LOW_PRESSURE = 1
    HIGH_VOLUME = 2
    LOW_VOLUME = 3
    HIGH_RESP_RATE = 4
    LOW_RESP_RATE = 5

