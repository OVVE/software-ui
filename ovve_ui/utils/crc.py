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
