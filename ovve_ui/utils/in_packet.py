from utils.params import Params
from utils.units import Units

class InPacket():

    def __init__(self) -> None:
        self.data={'sequence_count': 0,
                   'packet_version': 0,
                   'packet_type': 0,
                   'mode_value': 0,
                   'control_state': 0,
                   'battery_status': 0,
                   'reserved': 0,
                   'respiratory_rate_set': 0,
                   'respiratory_rate_measured': 0,
                   'tidal_volume_set': 0,
                   'tidal_volume_measured': 0,
                   'ie_ratio_set': 0,
                   'ie_ratio_measured': 0,
                   'peep_value_measured': 0,
                   'peak_pressure_measured': 0,
                   'plateau_value_measurement': 0,
                   'pressure_set': 0,
                   'pressure_measured': 0,
                   'flow_measured': 0,
                   'volume_in_measured': 0,
                   'volume_out_measured': 0,
                   'volume_rate_measured': 0,
                   'high_pressure_limit_set': 0,
                   'low_pressure_limit_set': 0,
                   'high_volume_limit_set': 0,
                   'low_volume_limit_set': 0,
                   'high_respiratory_rate_limit_set': 0,
                   'low_respiratory_rate_limit_set': 0,
                   'alarm_bits': 0,
                   'crc': 0,
                   'run_state': 0
                   }

    # byteData must have already been checked for proper length and crc
    def from_bytes(self, byteData: bytes) -> None:
        self.data['sequence_count']=int.from_bytes(byteData[0:2], byteorder='little')
        self.data['packet_version']=byteData[2]
        self.data['run_state'] = byteData[3] & (1 << 7)
        self.data['mode_value']= byteData[3] & 0x7F
        self.data['respiratory_rate_measured']=int.from_bytes(byteData[4:8], byteorder='little')
        self.data['respiratory_rate_set']=int.from_bytes(byteData[8:12], byteorder='little')
        self.data['tidal_volume_measured']=int.from_bytes(byteData[12:16], byteorder='little', signed=True)
        self.data['tidal_volume_set']=int.from_bytes(byteData[16:20], byteorder='little', signed=True)
        self.data['ie_ratio_measured']=int.from_bytes(byteData[20:24], byteorder='little')
        self.data['ie_ratio_set']=int.from_bytes(byteData[24:28], byteorder='little')
        self.data['peep_value_measured']=int.from_bytes(byteData[28:32], byteorder='little', signed=True)
        self.data['peak_pressure_measured']=int.from_bytes(byteData[32:36], byteorder='little', signed=True)
        self.data['plateau_value_measured']=int.from_bytes(byteData[36:40], byteorder='little', signed=True)
        self.data['pressure_measured']=int.from_bytes(byteData[40:44], byteorder='little', signed=True)
        self.data['flow_measured']=int.from_bytes(byteData[44:48], byteorder='little', signed=True)
        self.data['volume_in_measured']=int.from_bytes(byteData[48:52], byteorder='little', signed=True)
        self.data['volume_out_measured']=int.from_bytes(byteData[52:56], byteorder='little', signed=True)
        self.data['volume_rate_measured']=int.from_bytes(byteData[56:60], byteorder='little', signed=True)
        self.data['control_state']=byteData[60]
        self.data['battery_level']=byteData[61]
        self.data['reserved']=int.from_bytes(byteData[62:64], byteorder='little')
        self.data['alarm_bits']=int.from_bytes(byteData[64:68], byteorder='little')
        self.data['crc']=int.from_bytes(byteData[68:], byteorder='little')


    def to_params(self) -> Params:
        params = Params()
        params.run_state = self.data['run_state']
        params.seq_num = self.data['sequence_count']
        params.packet_version = self.data['packet_version']
        params.mode = self.data['mode_value']
        params.resp_rate_meas = self.data['respiratory_rate_measured']
        params.resp_rate_set = self.data['respiratory_rate_set']
        params.tv_meas = Units.ecu_to_ml(self.data['tidal_volume_measured'])
        params.tv_set = Units.ecu_to_ml(self.data['tidal_volume_set'])
        params.ie_ratio_meas = self.data['ie_ratio_measured']
        params.ie_ratio_set = self.data['ie_ratio_set']
        params.peep = Units.ecu_to_cmh2o(self.data['peep_value_measured'])
        params.ppeak = Units.ecu_to_cmh2o(self.data['peak_pressure_measured'])
        params.pplat = Units.ecu_to_cmh2o(self.data['plateau_value_measured'])
        params.pressure= Units.ecu_to_cmh2o(self.data['pressure_measured'])
        params.flow = Units.ecu_to_slm(self.data['flow_measured'])
        params.tv_insp = Units.ecu_to_ml(self.data['volume_in_measured'])
        params.tv_exp = Units.ecu_to_ml(self.data['volume_out_measured'])
        params.tv_rate = Units.ecu_to_ml(self.data['volume_rate_measured'])
        params.battery_level = self.data['battery_level']
        return params

