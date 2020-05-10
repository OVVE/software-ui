from utils.params import Params
from utils.units import Units

class InPacket():
    def __init__(self) -> None:
        self.data={ 'mode_value': 0,                
                    'respiratory_rate_measured': 0, 
                    'respiratory_rate_set': 0,      
                    'tidal_volume_measured': 0,     
                    'tidal_volume_set': 0,          
                    'ie_ratio_measured': 0,         
                    'ie_ratio_set': 0,              
                    'peep_value_measured': 0,       
                    'peak_pressure_measured': 0,    
                    'plateau_value_measured': 0,    
                    'pressure_measured': 0,         
                    'flow_measured': 0,             
                    'volume_in_measured': 0,        
                    'volume_out_measured': 0,       
                    'volume_rate_measured': 0,      
                    'control_state': 0,             
                    'battery_level': 0,             
                    'reserved': 0,                  
                    'alarm_bits': 0,                
                    'run_state': 0                  
                 }


    # byteData must have already been checked for proper length and crc
    def from_bytes(self, byteData: bytes) -> None:
        self.data['run_state'] = byteData[0] & (1 << 7)
        self.data['mode_value']= byteData[0] & 0x7F
        self.data['respiratory_rate_measured']=int.from_bytes(byteData[1:5], byteorder='little')
        self.data['respiratory_rate_set']=int.from_bytes(byteData[5:9], byteorder='little')
        self.data['tidal_volume_measured']=int.from_bytes(byteData[9:13], byteorder='little', signed=True)
        self.data['tidal_volume_set']=int.from_bytes(byteData[13:17], byteorder='little', signed=True)
        
        ie_measured_fixed = int.from_bytes(byteData[17:21], byteorder='little')
        ie_measured_fraction = self.ie_fixed_to_fraction(ie_measured_fixed)
        self.data['ie_ratio_measured'] = ie_measured_fraction

        ie_set_fixed = int.from_bytes(byteData[21:25], byteorder='little')
        ie_set_fraction = self.ie_fixed_to_fraction(ie_set_fixed)
        self.data['ie_ratio_set'] = ie_set_fraction

        self.data['peep_value_measured']=int.from_bytes(byteData[25:29], byteorder='little', signed=True)
        self.data['peak_pressure_measured']=int.from_bytes(byteData[29:33], byteorder='little', signed=True)
        self.data['plateau_value_measured']=int.from_bytes(byteData[33:37], byteorder='little', signed=True)
        self.data['pressure_measured']=int.from_bytes(byteData[37:41], byteorder='little', signed=True)
        self.data['flow_measured']=int.from_bytes(byteData[41:45], byteorder='little', signed=True)
        self.data['volume_in_measured']=int.from_bytes(byteData[45:49], byteorder='little', signed=True)
        self.data['volume_out_measured']=int.from_bytes(byteData[49:53], byteorder='little', signed=True)
        self.data['volume_rate_measured']=int.from_bytes(byteData[53:57], byteorder='little', signed=True)
        self.data['control_state']=byteData[57]
        self.data['battery_level']=byteData[58]
        self.data['reserved']=int.from_bytes(byteData[59:61], byteorder='little')
        self.data['alarm_bits']=int.from_bytes(byteData[61:65], byteorder='little')


    def to_params(self,sequenceNo) -> Params:
        params = Params()
        params.run_state = self.data['run_state']
        params.seq_num = sequenceNo
        params.packet_version = 4
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


    def ie_fixed_to_fraction(self, n: int) -> float:
        if n == 0:
            return 0

        if (n <= 128):
            i = 1.0
            e = (256 / float(n)) - 1
        else:
            i = (float(n) / 256) / (1 - float(n) / 256)
            e = 1.0
        
        if e == 0:
            return 0
        else:
            return i / e
       
    