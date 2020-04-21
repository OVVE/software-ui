from utils.crc import CRC
from utils.logger import Logger
import struct


class OutPacket():
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        self.crc = CRC(logger)
        self.data = {'sequence_count': 0,               # bytes 0 - 1 - rpi unsigned short int
            'packet_version': 1,                         # byte 2      - rpi unsigned char
            'mode_value': 0,                             # byte 3      - rpi unsigned char
            'respiratory_rate_set': 0, # bytes 5 - 8 - rpi unsigned int
            'tidal_volume_set':  0,         # bytes 8 - 11
            'ie_ratio_set':  0,             # bytes 12 - 15
            'alarm_bits':   0,              # bytes 16 - 19
            'crc':   0 }                    # bytes 20 - 21 - rpi unsigned short int 

    def to_bytes(self) -> bytes:
        # create the return packet
        endian = "little"
        cmd_byteData = b""
        #packet_version = 1

        cmd_byteData += bytes(self.data['sequence_count'].to_bytes(2, endian))
        cmd_byteData += bytes(self.data['packet_version'].to_bytes(1, endian))
        cmd_byteData += bytes(self.data['mode_value'].to_bytes(1, endian))
        cmd_byteData += bytes(self.data['respiratory_rate_set'].to_bytes(4, endian))
        cmd_byteData += bytes(self.data['tidal_volume_set'].to_bytes(4, endian))
        cmd_byteData += bytes(self.data['ie_ratio_set'].to_bytes(4, endian))
        # TO DO set alarmbits correctly if sequence or CRC failed
        cmd_byteData += bytes(self.data['alarm_bits'].to_bytes(4, endian))

        #Get CRC
        calcCRC = self.crc.crccitt(cmd_byteData.hex())
        # flip the bits - note that this will be 32 bit hex - do we will only send the first 2 later
        CRCtoSend = struct.pack('<Q', int(calcCRC, base=16))

        #send only 2 bytes
        cmd_byteData += CRCtoSend[0:2]

        return cmd_byteData
        
    def calculate_mode(self, in_mode, run_state) -> int:
         # VC_CMV_NON_ASSISTED_OFF = 0
        # VC_CMV_NON_ASSISTED_ON = 128
        # VC_CMV_ASSISTED_OFF = 1
        # VC_CMV_ASSISTED_OFF = 129
        # SIMV_OFF = 3
        # SIMV_ON = 130
        # get the updates from settings 
        # Set the mode value byte which also includes start bit
    

        return  (in_mode & 0x7f | (run_state << 7) & 0x80)

