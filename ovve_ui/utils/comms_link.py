import json
import random
import time
from threading import Thread
import serial
import sys
from time import sleep
import binascii
import crc16
import codecs

# BAUD = 38400
# PORT = "/dev/ttyACM0"
# SER_TIMEOUT = 0.055

from utils.comms_adapter import CommsAdapter
from utils.params import Params
from utils.settings import Settings


class CommsLink():
    def __init__(self, comms_adapter: CommsAdapter) -> None:
        self.comms_adapter = comms_adapter
        self.comms_adapter.set_comms_callback(self.update_settings)
        self.done = False
        self.settings = Settings()
        self.seqnum = 0
        self.packet_version = 1
        self.BAUD = 38400
        self.PORT = "/dev/ttyACM0"
        self.SER_TIMEOUT = 0.055
        self.ser = 0
        self.init_serial()

    def update_settings(self, settings_dict: dict) -> None:
        self.settings.from_dict(settings_dict)
        print("Got updated settings from UI")
        print(self.settings.to_JSON())

    #This function processes the serial data from Arduino and sends ACK

    def process_SerialData(self) -> None:
        params = Params()
        params_str = params.to_JSON()
        params_dict = json.loads(params_str)

        in_pkt={'sequence_count': 0,            # bytes 1 - 2 - rpi unsigned short int
            'packet_version': 0,             # byte 3      - rpi unsigned char
            'mode_value': 0,                 # byte 4      - rpi unsigned char
            'respiratory_rate_measured': 0, # bytes 5 - 8 - rpi unsigned int
            'respiratory_rate_set': 0,      # bytes 9 - 12
            'tidal_volume_measured': 0,     # bytes 13 - 16
            'tidal_volume_set': 0,          # bytes 17 - 20
            'ie_ratio_measured': 0,         # bytes 22 - 24
            'ie_ratio_set': 0,              # bytes 25 - 28
            'peep_value_measured': 0,       # bytes 29 - 32
            'peak_pressure_measured': 0,    # bytes 33 - 36
            'plateau_value_measurement': 0, # bytes 37 - 40
            'pressure_measured': 0,         # bytes 41 - 44
            'flow_measured': 0,             # bytes 45 - 48
            'volume_in_measured': 0,        # bytes 49 - 52
            'volume_out_measured': 0,       # bytes 53 - 56
            'volume_rate_measured': 0,      # bytes 57 - 60
            'control_state': 0,              # byte 61       - rpi unsigned char
            'battery_level': 0,              # byte 62
            'reserved': 0,                  # bytes 63 - 64 - rpi unsigned int
            'alarm_bits': 0,                # bytes 65 - 68
            'crc': 0 }                      # bytes 69 - 70 

        cmd_pkt = {'start_byte':255,
                    'sequence_count': 0,               # bytes 1 - 2 - rpi unsigned short int
                    'packet_version': 0,                         # byte 3      - rpi unsigned char
                    'mode_value': 0,                             # byte 4      - rpi unsigned char
                    'respiratory_rate_set': 0, # bytes 5 - 8 - rpi unsigned int
                    'tidal_volume_set':  0,         # bytes 9 - 12
                    'ie_ratio_set':  0,             # bytes 13 - 16
                    'alarm_bits':   0,              # bytes 17 - 20
                    'crc':   0 }                    # bytes 21 - 22 - rpi unsigned short int  
        
            
        self.ser.reset_input_buffer()
        error_count = 0

        while not self.done:
            
            byteData = self.read_all(self.ser, 71)
            #byteData = ser.read(72)
            #2 ways to print
            #print (byteData)  #raw will show ascii if can be decoded
            #hex only -- byte order is reversed
            #print(''.join(r'\x'+hex(letter)[2:] for letter in byteData))
            if byteData[0] == 0xff:
                #TO DO -- Map all packets to parameter structs
                in_pkt['sequence_count']=int.from_bytes(byteData[1:3], byteorder='little')
                in_pkt['packet_version']=byteData[3]
                in_pkt['mode_value']=byteData[4]
                in_pkt['respiratory_rate_measured']=int.from_bytes(byteData[5:9], byteorder='little')
                in_pkt['respiratory_rate_set']=int.from_bytes(byteData[9:13], byteorder='little')
                in_pkt['tidal_volume_measured']=int.from_bytes(byteData[13:17], byteorder='little')
                in_pkt['tidal_volume_set']=int.from_bytes(byteData[9:13], byteorder='little')
                in_pkt['ie_ratio_measured']=int.from_bytes(byteData[13:17], byteorder='little')
                in_pkt['ie_ratio_set']=int.from_bytes(byteData[9:13], byteorder='little')
                in_pkt['crc']=int.from_bytes(byteData[69:71], byteorder='little')
                
                print ('Received SEQ and CRC:')
                print (in_pkt['sequence_count'])
                print (in_pkt['crc'])
                self.seq_num = in_pkt['sequence_count']
                #self.settings.resp_rate = in_pkt['sequence_count']
                cmd_pkt['sequence_count'] = in_pkt['sequence_count']
                
            else:
                error_count = error_count + 1
                print ('drop packets count ' + str(error_count))


            endian = "little"
            cmd_byteData = b""
            start_byte = 0xFF
            packet_version = 1
           
            cmd_byteData += bytes(start_byte.to_bytes(1, endian))
            cmd_byteData += bytes(in_pkt['sequence_count'].to_bytes(2, endian))
            cmd_byteData += bytes(in_pkt['packet_version'].to_bytes(1, endian))
            cmd_byteData += bytes(cmd_pkt['mode_value'].to_bytes(1, endian))
            cmd_byteData += bytes(cmd_pkt['respiratory_rate_set'].to_bytes(4, endian))
            cmd_byteData += bytes(cmd_pkt['tidal_volume_set'].to_bytes(4, endian))
            cmd_byteData += bytes(cmd_pkt['ie_ratio_set'].to_bytes(4, endian))
            cmd_byteData += bytes(cmd_pkt['alarm_bits'].to_bytes(4, endian))
            calcCRC = self.crccitt(cmd_byteData.hex())
            print ('CALC CRC HEX and int: ')
            print(calcCRC)
            print(int(calcCRC, 16))
            cmd_pkt['crc']  = bytes.fromhex(calcCRC)

            #cmd_byteData += bytes(cmd_pkt['crc'].to_bytes(2, endian))
            cmd_byteData += cmd_pkt['crc']

            self.ser.write(cmd_byteData)
            
            print("Sent back SEQ and CRC: ")
            
            print (int.from_bytes(cmd_byteData[1:3], byteorder='little'))
            print (int.from_bytes(cmd_byteData[21:], byteorder='big'))

            params_dict['run_state'] = self.settings.run_state
            params_dict['seq_num'] = self.seqnum
            params_dict['packet_version'] = self.packet_version
            params_dict['mode'] = self.settings.mode
            params_dict['resp_rate_meas'] = self.settings.resp_rate
            params_dict['resp_rate_set'] = self.settings.resp_rate
            params_dict['tv_meas'] = self.settings.tv
            params_dict['tv_set'] = self.settings.tv
            params_dict['ie_ratio_meas'] = self.settings.ie_ratio
            params_dict['ie_ratio_set'] = self.settings.ie_ratio
            params_dict['peep'] = random.randrange(3, 6)
            params_dict['ppeak'] = random.randrange(15, 20)
            params_dict['pplat'] = random.randrange(15, 20)
            params_dict['pressure'] = random.randrange(15, 20)
            params_dict['flow'] = random.randrange(15, 20)
            params_dict['tv_insp'] = random.randrange(475, 575)
            #params_dict['tv_exp'] = random.randrange(475, 575)
            #testing if actual data from arduino can be displayed in GUI
            params_dict['tv_exp'] = in_pkt['sequence_count']
            params_dict['tv_min'] = random.randrange(475, 575)
            params_dict['tv_min'] = random.randrange(475, 575)
            params_dict['control_state'] = 0
            params_dict['battery_level'] = 255
            self.comms_adapter.update_params(params_dict)

            #self.seqnum += 1
            #time.sleep(1)

    def init_serial(self):
    
        #global ser          #Must be declared in Each Function
        self.ser = serial.Serial()
        self.ser.baudrate = self.BAUD
        self.ser.port = self.PORT 
        #a little less than polling spped from arduino
        self.ser.timeout = self.SER_TIMEOUT
        self.ser.open()          #Opens SerialPort

        # print port open or closed
        if self.ser.isOpen():
            print ('Open: ' + self.ser.portstr)
        sleep(1)

    def crccitt(self, hex_string):
        byte_seq = binascii.unhexlify(hex_string)
        crc = crc16.crc16xmodem(byte_seq, 0xffff)
        return '{:04X}'.format(crc & 0xffff)

    def read_all(self, port, chunk_size=200):
        """Read all characters on the serial port and return them."""
        if not port.timeout:
            raise TypeError('Port needs to have a timeout set!')

        read_buffer = b''

        while True:
            # Read in chunks. Each chunk will wait as long as specified by
            # timeout. Increase chunk_size to fail quicker
            byte_chunk = port.read(size=chunk_size)
            read_buffer += byte_chunk
            if not len(byte_chunk) == chunk_size:
                break

        return read_buffer

    def simulate_params(self) -> None:
        params = Params()
        params_str = params.to_JSON()
        params_dict = json.loads(params_str)

        while not self.done:
            params_dict['run_state'] = self.settings.run_state
            params_dict['seq_num'] = self.seqnum
            params_dict['packet_version'] = self.packet_version
            params_dict['mode'] = self.settings.mode
            params_dict['resp_rate_meas'] = self.settings.resp_rate
            params_dict['resp_rate_set'] = self.settings.resp_rate
            params_dict['tv_meas'] = self.settings.tv
            params_dict['tv_set'] = self.settings.tv
            params_dict['ie_ratio_meas'] = self.settings.ie_ratio
            params_dict['ie_ratio_set'] = self.settings.ie_ratio
            params_dict['peep'] = random.randrange(3, 6)
            params_dict['ppeak'] = random.randrange(15, 20)
            params_dict['pplat'] = random.randrange(15, 20)
            params_dict['pressure'] = random.randrange(15, 20)
            params_dict['flow'] = random.randrange(15, 20)
            params_dict['tv_insp'] = random.randrange(475, 575)
            params_dict['tv_exp'] = random.randrange(475, 575)
            params_dict['tv_min'] = random.randrange(475, 575)
            params_dict['tv_min'] = random.randrange(475, 575)
            params_dict['control_state'] = 0
            params_dict['battery_level'] = 255
            self.comms_adapter.update_params(params_dict)

            self.seqnum += 1
            time.sleep(1)





    def start(self) -> None:
        t = Thread(target=self.process_SerialData, args=())
        t.start()

    def stop(self) -> None:
        self.done = True
