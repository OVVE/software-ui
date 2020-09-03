 
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


from enum import IntEnum

class ControlState(IntEnum):
    UNCALIBRATED = 0x00
    IDLE = 0x01
    BEGIN_INHALATION = 0x02
    INHALATION = 0x03
    BEGIN_HOLD_IN = 0x04
    HOLD_IN = 0x05
    BEGIN_EXHALATION = 0x06
    EXHALATION = 0x07
    HOME = 0x08
    HALT = 0x09
    SENSOR_CALIBRATION = 0x0a
    SENSOR_CALIBRATION_DONE = 0x0b
