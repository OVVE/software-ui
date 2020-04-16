
import crc16

class CRC():
    def __init__():
        pass
    
    def check_crc(self crcbytes: bytes) -> bool: 
         # calculate CRC 
        rcvdCRC = int.from_bytes(byteData[68:], byteorder='little')
        # reverse HEX order
        calcRcvCRC = self.crccitt(byteData[0:68].hex())
        calcRcvCRC = int(calcRcvCRC, 16)
        if calcRcvCRC != rcvdCRC:
            return False
        
        return True


    def crccitt(self, hex_string):
        byte_seq = binascii.unhexlify(hex_string)
        crc = crc16.crc16xmodem(byte_seq, 0xffff)
        return '{:04X}'.format(crc & 0xffff)