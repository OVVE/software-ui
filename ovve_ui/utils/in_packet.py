from utils.params import Params

class InPacket():
    def __init__(self):
        self.data={'sequence_count': 0,            # bytes  0- 1 - rpi unsigned short int
                    'packet_version': 0,             # byte 2      - rpi unsigned char
                    'mode_value': 0,                 # byte 3      - rpi unsigned char
                    'respiratory_rate_measured': 0, # bytes 4 - 7 - rpi unsigned int
                    'respiratory_rate_set': 0,      # bytes 8 - 11
                    'tidal_volume_measured': 0,     # bytes 12 - 15
                    'tidal_volume_set': 0,          # bytes 16 - 19
                    'ie_ratio_measured': 0,         # bytes 20 - 23
                    'ie_ratio_set': 0,              # bytes 24 - 27
                    'peep_value_measured': 0,       # bytes 28 - 31
                    'peak_pressure_measured': 0,    # bytes 32 - 35
                    'plateau_value_measurement': 0, # bytes 36 - 39
                    'pressure_measured': 0,         # bytes 40 - 43
                    'flow_measured': 0,             # bytes 44 - 47
                    'volume_in_measured': 0,        # bytes 48 - 51
                    'volume_out_measured': 0,       # bytes 52 - 55
                    'volume_rate_measured': 0,      # bytes 56 - 59
                    'control_state': 0,              # byte 60       - rpi unsigned char
                    'battery_level': 0,              # byte 61
                    'reserved': 0,                  # bytes 62 - 63 - rpi unsigned int
                    'alarm_bits': 0,                # bytes 64 - 67
                    'crc': 0 }                      # bytes 68 - 69 


    # byteData must have already been checked for proper length and crc
    def from_bytes(byteData: bytes) -> None:
        self.data['sequence_count']=int.from_bytes(byteData[0:2], byteorder='little')
        self.data['packet_version']=byteData[2]
        self.data['mode_value']=byteData[3]
        self.data['respiratory_rate_measured']=int.from_bytes(byteData[4:8], byteorder='little')
        self.data['respiratory_rate_set']=int.from_bytes(byteData[8:12], byteorder='little')
        self.data['tidal_volume_measured']=int.from_bytes(byteData[12:16], byteorder='little')
        self.data['tidal_volume_set']=int.from_bytes(byteData[16:20], byteorder='little')
        self.data['ie_ratio_measured']=int.from_bytes(byteData[20:24], byteorder='little')
        self.data['ie_ratio_set']=int.from_bytes(byteData[24:28], byteorder='little')
        self.data['peep_value_measured']=int.from_bytes(byteData[28:32], byteorder='little')
        self.data['peak_pressure_measured']=int.from_bytes(byteData[32:36], byteorder='little')
        self.data['plateau_value_measured']=int.from_bytes(byteData[36:40], byteorder='little')
        self.data['pressure_measured']=int.from_bytes(byteData[40:44], byteorder='little')
        self.data['flow_measured']=int.from_bytes(byteData[44:48], byteorder='little')
        self.data['volume_in_measured']=int.from_bytes(byteData[48:52], byteorder='little')
        self.data['volume_out_measured']=int.from_bytes(byteData[52:56], byteorder='little')
        self.data['volume_rate_measured']=int.from_bytes(byteData[56:60], byteorder='little')
        self.data['control_state']=byteData[60]
        self.data['battery_level']=byteData[61]
        self.data['reserved']=int.from_bytes(byteData[62:64], byteorder='little')
        self.data['alarm_bits']=int.from_bytes(byteData[64:68], byteorder='little')
        self.data['crc']=int.from_bytes(byteData[68:], byteorder='little')


    def to_params() -> Params:
        params = Params()
        params.seq_num = self.data['sequence_count']
        params.packet_version = self.data['packet_version']
        params.mode = self.data['mode_value']
        params.resp_rate_meas = self.data['respiratory_rate_measured']
        params.resp_rate_set = self.data['respiratory_rate_set']
        params.tv_meas = self.data['tidal_volume_measured']
        params.tv_set = self.data['tidal_volume_set']
        params.ie_ratio_meas = in_self.data['ie_ratio_measured']
        params.ie_ratio_set = in_self.data['ie_ratio_set']
        params.peep = self.data['peep_value_measured']
        params.ppeak = self.data['peak_pressure_measured']
        params.pplat = self.data['plateau_value_measurement']
        params.pressure= self.data['pressure_measured']
        params.flow = self.data['volume_in_measured']
        params.tv_exp = self.data['volume_out_measured']
        params.tv_rate = self.data['volume_rate_measured']
        params.battery_level = self.data['battery_level']

        return params