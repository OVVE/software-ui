import struct

from utils.crc import CRC

class OutPacket():
    def __init__(self) -> None:
        self.crc = CRC()
        self.data = {
            'mode_value': 0,                             # byte 3      - rpi unsigned char
            'command': 0,
            'reserved': 0,
            'respiratory_rate_set': 0,
            'tidal_volume_set': 0,
            'ie_ratio_set': 0,
            'pressure_set': 0,
            'high_pressure_limit_set': 0,
            'low_pressure_limit_set': 0,
            'high_volume_limit_set': 0,
            'low_volume_limit_set': 0,
            'high_respiratory_rate_limit_set': 0,
            'low_respiratory_rate_limit_set': 0,
            'alarm_bits':   0,              # bytes 16 - 19
            }                    # bytes 20 - 21 - rpi unsigned short int 

    def to_bytes(self) -> bytes:
        # create the return packet
        endian = "little"
        cmd_byteData = b""
        #packet_version = 1
        cmd_byteData += bytes(self.data['mode_value'].to_bytes(1, endian))        
        cmd_byteData += bytes(self.data['command'].to_bytes(1, endian))  
        cmd_byteData += bytes(self.data['reserved'].to_bytes(2, endian))   
        cmd_byteData += bytes(self.data['respiratory_rate_set'].to_bytes(2, endian))   
        cmd_byteData += bytes(self.data['tidal_volume_set'].to_bytes(2, endian))     
        cmd_byteData += bytes(self.data['ie_ratio_set'].to_bytes(2, endian))  
        cmd_byteData += bytes(self.data['pressure_set'].to_bytes(2, endian))
        cmd_byteData += bytes(self.data['high_pressure_limit_set'].to_bytes(2, endian))
        cmd_byteData += bytes(self.data['low_pressure_limit_set'].to_bytes(2, endian))         
        cmd_byteData += bytes(self.data['high_volume_limit_set'].to_bytes(2, endian))  
        cmd_byteData += bytes(self.data['low_volume_limit_set'].to_bytes(2, endian))
        cmd_byteData += bytes(self.data['high_respiratory_rate_limit_set'].to_bytes(2, endian))
        cmd_byteData += bytes(self.data['low_respiratory_rate_limit_set'].to_bytes(2, endian))        
        # TO DO set alarmbits correctly if sequence or CRC failed
        cmd_byteData += bytes(self.data['alarm_bits'].to_bytes(4, endian))

        return cmd_byteData
        
    def pack_command(self, run_state, upgrade_fw) -> int:
        return (((run_state == 1) << 0) |
                ((upgrade_fw == 1) << 4))


    def ie_fraction_to_fixed(self, ie_fraction: float) -> int:
        # I:E -> int(I / (I + E) * 256) = n
        return int(1 / (1 + (1 / ie_fraction)) * 256)
