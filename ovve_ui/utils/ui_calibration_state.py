from enum import IntEnum

class UICalibrationState(IntEnum):
    UNCALIBRATED = 0
    SENSOR_CALIBRATION = 1
    CALIBRATION_PENDING = 2
    CALIBRATION_DONE = 3

