 
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


class Units():
    # Unit converts between common units

    # ECU measures flow in [0.1SLM]
    @staticmethod
    def ecu_to_slm(flow: int) -> float:
        return float(flow) * 0.01

    @staticmethod
    def slm_to_ecu(flow: float) -> int:
        return int(flow * 100)

    # ECU measures volume in [mL]
    @staticmethod
    def ecu_to_ml(vol: int) -> float:
        return float(vol)

    @staticmethod
    def ml_to_ecu(vol: float) -> int:
        return int(vol)

    # ECU measures pressure in [0.1mmH2O]
    @staticmethod
    def ecu_to_cmh2o(pres: int) -> float:
        return float(pres) * 0.01

    @staticmethod
    def cmh2o_to_ecu(pres: float) -> int:
        return int(pres * 100)
