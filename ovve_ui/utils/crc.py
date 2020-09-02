 
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


import crc16
import binascii
import logging


class CRC():
    def __init__(self) -> None:
        self.logger = logging.getLogger()
        pass

    def check_crc(self, byteData: bytes) -> bool:
        # calculate CRC
        rcvdCRC = int.from_bytes(byteData[54:], byteorder='little')
        # reverse HEX order
        calcRcvCRC = self.crccitt(byteData[0:54].hex())
        calcRcvCRC = int(calcRcvCRC, 16)
        if calcRcvCRC != rcvdCRC:
            self.logger.warning(str(byteData))
            self.logger.warning("CRC check failed! rcvd: " + str(rcvdCRC) +
                                " calc: " + str(calcRcvCRC))
            return False

        return True

    def crccitt(self, hex_string):
        byte_seq = binascii.unhexlify(hex_string)
        crc = crc16.crc16xmodem(byte_seq, 0xffff)
        return '{:04X}'.format(crc & 0xffff)
