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
        self.crcFailCnt = 0
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
        prevSeq = 0
        error_count = 0
        currentSeq = 0
        validData = False

        in_pkt={'sequence_count': 0,            # bytes  0- 1 - rpi unsigned short int
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

        cmd_pkt = {'sequence_count': 0,               # bytes 0 - 1 - rpi unsigned short int
                    'packet_version': 1,                         # byte 2      - rpi unsigned char
                    'mode_value': 0,                             # byte 3      - rpi unsigned char
                    'respiratory_rate_set': 0, # bytes 5 - 8 - rpi unsigned int
                    'tidal_volume_set':  0,         # bytes 8 - 11
                    'ie_ratio_set':  0,             # bytes 12 - 15
                    'alarm_bits':   0,              # bytes 16 - 19
                    'crc':   0 }                    # bytes 20 - 21 - rpi unsigned short int  
            
        self.ser.reset_input_buffer()

        while not self.done:
            
            byteData = self.read_all(self.ser, 70)
            # DEBUG
            # 2 ways to print for debugging 
            # print (byteData)  #raw will show ascii if can be decoded
            # hex only -- byte order is reversed
            # print(''.join(r'\x'+hex(letter)[2:] for letter in byteData))
            # END DEBUG
            if byteData[0:2] == b'\x00\x00':
                prevSeq = -1 
                currentSeq = int.from_bytes(byteData[0:2], byteorder='little')
            else:
                prevSeq = (int.from_bytes(byteData[0:2], byteorder='little') - 1)
                currentSeq = int.from_bytes(byteData[0:2], byteorder='little')
                
                #TO DO -- Map all packets to parameter structs
                 
            if  currentSeq !=  ( prevSeq + 1) :
                print ("There appears to be Sequence Error")
                print (currentSeq)
                print (prevSeq)

            # calculate CRC instead of
            rcvdCRC = int.from_bytes(byteData[68:], byteorder='little')


            # rcvdCRC = (int.from_bytes(byteData[0:2], byteorder='little')).hex()
            calcRcvCRC = self.crccitt(byteData[0:68].hex())
            calcRcvCRC = int(calcRcvCRC, 16)
            if calcRcvCRC != rcvdCRC:
                print ("CRC check failed")
                self.crcFailCnt += self.crcFailCnt
                print (rcvdCRC)
                print (calcRcvCRC)
                cmd_pkt['sequence_count'] = in_pkt['sequence_count']

            else:
                validData = True
                in_pkt['sequence_count']=int.from_bytes(byteData[0:2], byteorder='little')
                in_pkt['packet_version']=byteData[2]
                in_pkt['mode_value']=byteData[3]
                in_pkt['respiratory_rate_measured']=int.from_bytes(byteData[4:8], byteorder='little')
                in_pkt['respiratory_rate_set']=int.from_bytes(byteData[8:12], byteorder='little')
                in_pkt['tidal_volume_measured']=int.from_bytes(byteData[12:16], byteorder='little')
                in_pkt['tidal_volume_set']=int.from_bytes(byteData[16:20], byteorder='little')
                in_pkt['ie_ratio_measured']=int.from_bytes(byteData[20:24], byteorder='little')
                in_pkt['ie_ratio_set']=int.from_bytes(byteData[24:28], byteorder='little')
                in_pkt['peep_value_measured']=int.from_bytes(byteData[28:32], byteorder='little')
                in_pkt['peak_pressure_measured']=int.from_bytes(byteData[32:36], byteorder='little')
                in_pkt['plateau_value_measured']=int.from_bytes(byteData[36:40], byteorder='little')
                in_pkt['pressure_measured']=int.from_bytes(byteData[40:44], byteorder='little')
                in_pkt['flow_measured']=int.from_bytes(byteData[44:48], byteorder='little')
                in_pkt['volume_in_measured']=int.from_bytes(byteData[48:52], byteorder='little')
                in_pkt['volume_out_measured']=int.from_bytes(byteData[52:56], byteorder='little')
                in_pkt['volume_rate_measured']=int.from_bytes(byteData[56:60], byteorder='little')
                in_pkt['control_state']=byteData[60]
                in_pkt['battery_level']=byteData[61]
                in_pkt['reserved']=int.from_bytes(byteData[62:64], byteorder='little')
                in_pkt['alarm_bits']=int.from_bytes(byteData[64:68], byteorder='little')
                in_pkt['crc']=int.from_bytes(byteData[68:], byteorder='little')
                
                # DEBUG
                print ('Received SEQ and CRC:')
                print (in_pkt['sequence_count'])
                print (in_pkt['crc'])
                #END DEBUG
                # UI may need this keeping
                self.seq_num = in_pkt['sequence_count']
                # Needed for the return packet
                cmd_pkt['sequence_count'] = in_pkt['sequence_count']
                # ENDIF

            # ecu_settings_dict = {'to_JSON':ecu_settings_str, 'run_state': 0,'mode': 0,'tv': 0,'resp_rate':0 ,'ie_ratio': 0}
            # self.comms_adapter.update_settings()

            # create the return packet
            endian = "little"
            cmd_byteData = b""
            #packet_version = 1

            # get the updates from settings TODO: Make this event driven and only when callbackis called
            cmd_pkt['mode_value'] = self.settings.mode
            cmd_pkt['respiratory_rate_set'] = self.settings.resp_rate
            cmd_pkt['tidal_volume_set'] = self.settings.tv
            cmd_pkt['ie_ratio_set'] = self.settings.ie_ratio

            cmd_byteData += bytes(cmd_pkt['sequence_count'].to_bytes(2, endian))
            cmd_byteData += bytes(cmd_pkt['packet_version'].to_bytes(1, endian))
            cmd_byteData += bytes(cmd_pkt['mode_value'].to_bytes(1, endian))
            cmd_byteData += bytes(cmd_pkt['respiratory_rate_set'].to_bytes(4, endian))
            cmd_byteData += bytes(cmd_pkt['tidal_volume_set'].to_bytes(4, endian))
            cmd_byteData += bytes(cmd_pkt['ie_ratio_set'].to_bytes(4, endian))
            
            # TO DO set alarmbits correctly if sequence or CRC failed
            cmd_byteData += bytes(cmd_pkt['alarm_bits'].to_bytes(4, endian))
            calcSendCRC = self.crccitt(cmd_byteData.hex())
            # DEBUG
            # print ('CALC sent CRC HEX and int: ')
            # print(calcSendCRC)
            # print(int(calcSendCRC, 16))
            #end DEBUG
            cmd_pkt['crc']  = bytes.fromhex(calcSendCRC)
            cmd_byteData += cmd_pkt['crc']
            try:
                self.ser.write(cmd_byteData)
            except:
                print("Faile to write to serial")
            
            # DEBUG
            print ("Packet Written:")
            print(''.join(r'\x'+hex(letter)[2:] for letter in cmd_byteData))
            print("Sent back SEQ and CRC: ")
            print (int.from_bytes(cmd_byteData[0:2], byteorder='little'))
            print (int.from_bytes(cmd_byteData[20:], byteorder='big'))
            # END DEBUG

            #Update dict only if there is valid data
            if validData == True:
                # any settings set will not retunr correctly yet until Arduino sets set values correctly
                # We can use the settings values like in simulator if so desired or maybe compare them
                params_dict['run_state'] = self.settings.run_state
                params_dict['seq_num'] = in_pkt['sequence_count']
                params_dict['packet_version'] = in_pkt['packet_version']
                params_dict['mode'] = in_pkt['mode_value']
                params_dict['resp_rate_meas'] = in_pkt['respiratory_rate_measured']
                params_dict['resp_rate_set'] = in_pkt['respiratory_rate_set']
                params_dict['tv_meas'] = in_pkt['tidal_volume_measured']
                params_dict['tv_set'] = in_pkt['tidal_volume_set']
                params_dict['ie_ratio_meas'] = in_pkt['ie_ratio_measured']
                params_dict['ie_ratio_set'] = in_pkt['ie_ratio_set']
                params_dict['peep'] = in_pkt['peep_value_measured']
                params_dict['ppeak'] = in_pkt['peak_pressure_measured']
                params_dict['pplat'] = in_pkt['plateau_value_measurement']
                params_dict['pressure'] = in_pkt['pressure_measured']
                params_dict['flow'] = in_pkt['flow_measured']
                params_dict['tv_insp'] = in_pkt['volume_in_measured']
                params_dict['tv_exp'] = in_pkt['volume_out_measured']
                params_dict['tv_rate'] = in_pkt['volume_rate_measured']
                # Not sure what is tv_min keeping it like in sumulator for now
                params_dict['tv_min'] = random.randrange(475, 575)
                params_dict['control_state'] = 0
                params_dict['battery_level'] = in_pkt['battery_level']
                # is this class variable necessary?
                # self. seqnum = params_dict['seq_num']
                self.comms_adapter.update_params(params_dict)
                # we got here
                # print ("UI parameters updated")

            #
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


    def start(self) -> None:
        t = Thread(target=self.process_SerialData, args=())
        t.start()

    def stop(self) -> None:
        self.done = True