import json
import random
import time
from threading import Thread, Lock
import serial
import sys
from time import sleep
import binascii
import crc16
import codecs
import struct

from utils.params import Params
from utils.settings import Settings
from utils.serial_watchdog import Watchdog
from PyQt5.QtCore import QThread, pyqtSignal


class CommsLink(QThread):
    new_params = pyqtSignal(dict)
    new_alarms = pyqtSignal(dict)

    
    def __init__(self) -> None:
        QThread.__init__(self)
        self.done = False
        self.settings = Settings()
        self.settings_lock = Lock()
        self.seqnum = 0
        self.packet_version = 1
        self.BAUD = 38400
        self.PORT = "/dev/ttyUSB0"
        self.SER_TIMEOUT = 0.065
        self.SER_WRITE_TIMEOUT = 0.03
        self.SER_INTER_TIMEOUT = 0.01
        self.ser = 0
        self.crcFailCnt = 0
        self.setting_lock = Lock()
        self.runState_fromECU = 0
 
        self.cmd_pkt = {'sequence_count': 0,               # bytes 0 - 1 - rpi unsigned short int
                    'packet_version': 1,                         # byte 2      - rpi unsigned char
                    'mode_value': 0,                             # byte 3      - rpi unsigned char
                    'respiratory_rate_set': 0, # bytes 5 - 8 - rpi unsigned int
                    'tidal_volume_set':  0,         # bytes 8 - 11
                    'ie_ratio_set':  0,             # bytes 12 - 15
                    'alarm_bits':   0,              # bytes 16 - 19
                    'crc':   0 }                    # bytes 20 - 21 - rpi unsigned short int  
        self.in_pkt={'sequence_count': 0,            # bytes  0- 1 - rpi unsigned short int
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

        

    def update_settings(self, settings_dict: dict) -> None:
        self.settings_lock.acquire()
        self.settings.from_dict(settings_dict)
        self.settings_lock.release()
        print("Got updated settings from UI")
        print(self.settings.to_JSON())

    #This function processes the serial data from Arduino and sends ACK

    def calculate_runstate(self, mode_value):
        # VC_CMV_NON_ASSISTED_OFF = 0
        # VC_CMV_NON_ASSISTED_ON = 1
        # VC_CMV_ASSISTED_OFF = 2
        # VC_CMV_ASSISTED_OFF = 3
        # SIMV_OFF = 4
        # SIMV_ON = 5
        
        startBit = None

        if mode_value == 0:
            startBit = 0
        elif mode_value == 1:
            startBit = 1
        elif mode_value == 2:
            startBit = 0
        elif mode_value == 3:
            startBit == 1
        elif mode_value == 4:
            startBit == 0
        elif mode_value == 5:
            startBit = 1
        else:
            startBit = 0
        return startBit

    def process_SerialData(self) -> None:
        params = Params()
        params_str = params.to_JSON()
        params_dict = json.loads(params_str)
        prevSeq = 0
        error_count = 0
        currentSeq = 0
        validData = False
        ValidPkt = 0
   
        self.ser.reset_input_buffer()
        byteData = b''
        
        while not self.done:
            
            byteData = self.read_all(self.ser, 70)
            if len(bytearray(byteData)) != 70:
                print("reread")
                byteData = self.read_all(self.ser, 70)
            else:
                ValidPkt += ValidPkt
            self.ser.flush()
            # DEBUG
            # 2 ways to print for debugging 
            # print (byteData)  #raw will show ascii if can be decoded
            # hex only -- byte order is reversed
            # print ("Packet Rcvd:")
            # print(''.join(r'\x'+hex(letter)[2:] for letter in byteData))
            print(len(bytearray(byteData)))
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

            # calculate CRC 
            rcvdCRC = int.from_bytes(byteData[68:], byteorder='little')
            # reverse HEX order
            calcRcvCRC = self.crccitt(byteData[0:68].hex())
            calcRcvCRC = int(calcRcvCRC, 16)
            if calcRcvCRC != rcvdCRC:
                print ("CRC check failed")
                self.crcFailCnt += self.crcFailCnt
                print (rcvdCRC)
                print (calcRcvCRC)
                error_count = error_count + 1
                print ('Dropped packets count ' + str(error_count))
                print ('Valid packets count ' + str(ValidPkt))
                validData = False
            else:
                validData = True
                self.in_pkt['sequence_count']=int.from_bytes(byteData[0:2], byteorder='little')
                self.in_pkt['packet_version']=byteData[2]
                self.in_pkt['mode_value']=byteData[3]
                self.in_pkt['respiratory_rate_measured']=int.from_bytes(byteData[4:8], byteorder='little')
                self.in_pkt['respiratory_rate_set']=int.from_bytes(byteData[8:12], byteorder='little')
                self.in_pkt['tidal_volume_measured']=int.from_bytes(byteData[12:16], byteorder='little')
                self.in_pkt['tidal_volume_set']=int.from_bytes(byteData[16:20], byteorder='little')
                self.in_pkt['ie_ratio_measured']=int.from_bytes(byteData[20:24], byteorder='little')
                self.in_pkt['ie_ratio_set']=int.from_bytes(byteData[24:28], byteorder='little')
                self.in_pkt['peep_value_measured']=int.from_bytes(byteData[28:32], byteorder='little')
                self.in_pkt['peak_pressure_measured']=int.from_bytes(byteData[32:36], byteorder='little')
                self.in_pkt['plateau_value_measured']=int.from_bytes(byteData[36:40], byteorder='little')
                self.in_pkt['pressure_measured']=int.from_bytes(byteData[40:44], byteorder='little')
                self.in_pkt['flow_measured']=int.from_bytes(byteData[44:48], byteorder='little')
                self.in_pkt['volume_in_measured']=int.from_bytes(byteData[48:52], byteorder='little')
                self.in_pkt['volume_out_measured']=int.from_bytes(byteData[52:56], byteorder='little')
                self.in_pkt['volume_rate_measured']=int.from_bytes(byteData[56:60], byteorder='little')
                self.in_pkt['control_state']=byteData[60]
                self.in_pkt['battery_level']=byteData[61]
                self.in_pkt['reserved']=int.from_bytes(byteData[62:64], byteorder='little')
                self.in_pkt['alarm_bits']=int.from_bytes(byteData[64:68], byteorder='little')
                self.in_pkt['crc']=int.from_bytes(byteData[68:], byteorder='little')
                # is there a need for this by the UI
                self.runState_fromECU = self.calculate_runstate(self.in_pkt['mode_value'] )
                # DEBUG
                print ('Received SEQ and CRC:')
                print (self.in_pkt['sequence_count'])
                print (self.in_pkt['crc'])
                print('current runstate  from ECU: ' + str(self.runState_fromECU))
                #END DEBUG

                # Needed for the return packet
                self.cmd_pkt['sequence_count'] = self.in_pkt['sequence_count']
                # ENDIF
            
            # Lock to prevent settings from being written in the middle of
            # creating the packet.
            self.settings_lock.acquire()
            # get the updates from settings 
            # Set the mode value byte which also includes start bit
            if self.settings.mode == 0 and self.settings.run_state == 0:
                self.cmd_pkt['mode_value'] = 0
            elif self.settings.mode == 0 and self.settings.run_state == 1:
                self.cmd_pkt['mode_value'] = 1
            elif self.settings.mode == 1 and self.settings.run_state == 0:
                self.cmd_pkt['mode_value'] = 2
            elif self.settings.mode == 1 and self.settings.run_state == 1:
                self.cmd_pkt['mode_value'] = 3
            elif self.settings.mode == 2 and self.settings.run_state == 0:
                self.cmd_pkt['mode_value'] = 4
            elif self.settings.mode == 2 and self.settings.run_state == 1:
                self.cmd_pkt['mode_value'] = 5
            else:
                self.cmd_pkt['mode_value'] = 0

            self.cmd_pkt['respiratory_rate_set'] = self.settings.resp_rate
            self.cmd_pkt['tidal_volume_set'] = self.settings.tv
            self.cmd_pkt['ie_ratio_set'] = self.settings.ie_ratio
            # release lock
            self.settings_lock.release()

            self.sendPkts(self.cmd_pkt['sequence_count'], self.in_pkt['crc'])
            #Update dict only if there is valid data
            if validData == True:
                # any settings set will not return correctly yet until Arduino sets set values correctly
                # We can use the settings values like in simulator if so desired or maybe compare them
                # RE: Run_state, we still need to implment getting this from Arduino. Currently I am just getting zero
                # When done, this will MSB off self.in_pkt['mode_value']
                params_dict['run_state'] = self.settings.run_state
                params_dict['seq_num'] = self.in_pkt['sequence_count']
                params_dict['packet_version'] = self.in_pkt['packet_version']
                params_dict['mode'] = self.in_pkt['mode_value']
                params_dict['resp_rate_meas'] = self.in_pkt['respiratory_rate_measured']
                params_dict['resp_rate_set'] = self.in_pkt['respiratory_rate_set']
                params_dict['tv_meas'] = self.in_pkt['tidal_volume_measured']
                params_dict['tv_set'] = self.in_pkt['tidal_volume_set']
                params_dict['ie_ratio_meas'] = self.in_pkt['ie_ratio_measured']
                params_dict['ie_ratio_set'] = self.in_pkt['ie_ratio_set']
                params_dict['peep'] = self.in_pkt['peep_value_measured']
                params_dict['ppeak'] = self.in_pkt['peak_pressure_measured']
                params_dict['pplat'] = self.in_pkt['plateau_value_measurement']
                params_dict['pressure'] = self.in_pkt['pressure_measured']
                params_dict['flow'] = self.in_pkt['flow_measured']
                params_dict['tv_insp'] = self.in_pkt['volume_in_measured']
                params_dict['tv_exp'] = self.in_pkt['volume_out_measured']
                params_dict['tv_rate'] = self.in_pkt['volume_rate_measured']
                params_dict['control_state'] = 0
                params_dict['battery_level'] = self.in_pkt['battery_level']
                self.new_params.emit(params_dict)


    def init_serial(self) -> False:

        self.ser = serial.Serial()
        self.ser.baudrate = self.BAUD
        self.ser.port = self.PORT 
        self.ser.timeout = self.SER_TIMEOUT
        self.ser.write_timeout = self.SER_WRITE_TIMEOUT
        
        try:
            
            if self.ser == None:
                self.ser.open()
                print ("Successfully connected to port %r." % self.ser.port)
                
                return True
            else:
                if self.ser.isOpen():
                    self.ser.close()
                    print ("Disconnected current connection.")
                    return False
                else:
                    self.ser.open()
                    print ("Connected to port %r." % self.ser.port)
                    return True
        except serial.SerialException:
            return False

    def crccitt(self, hex_string):
        byte_seq = binascii.unhexlify(hex_string)
        crc = crc16.crc16xmodem(byte_seq, 0xffff)
        return '{:04X}'.format(crc & 0xffff)

    def read_all(self, port, chunk_size=200):
        """Read all characters on the serial port and return them."""
        if not port.isOpen():
            raise SerialException('Serial is diconnected') 
        if not port.timeout:
            raise TypeError('Port needs to have a timeout set!')

        read_buffer = b''

        while True:
            # Read in chunks. Each chunk will wait as long as specified by
            # timeout. Increase chunk_size to fail quicker
            byte_chunk = port.read(size=chunk_size)
            #sleep(0.001)
            read_buffer += byte_chunk
            if not len(byte_chunk) == chunk_size:
                break
        #port.reset_input_buffer()
        return read_buffer

    def sendPkts(self, seq_cnt, crc):

        # create the return packet
        endian = "little"
        cmd_byteData = b""
        #packet_version = 1

        cmd_byteData += bytes(self.cmd_pkt['sequence_count'].to_bytes(2, endian))
        cmd_byteData += bytes(self.cmd_pkt['packet_version'].to_bytes(1, endian))
        cmd_byteData += bytes(self.cmd_pkt['mode_value'].to_bytes(1, endian))
        cmd_byteData += bytes(self.cmd_pkt['respiratory_rate_set'].to_bytes(4, endian))
        cmd_byteData += bytes(self.cmd_pkt['tidal_volume_set'].to_bytes(4, endian))
        cmd_byteData += bytes(self.cmd_pkt['ie_ratio_set'].to_bytes(4, endian))
        # TO DO set alarmbits correctly if sequence or CRC failed
        cmd_byteData += bytes(self.cmd_pkt['alarm_bits'].to_bytes(4, endian))
        #Get CRC
        calcCRC = self.crccitt(cmd_byteData.hex())
        # flip the bits - note that this will be 32 bit hex - do we will only send the first 2 later
        CRCtoSend = struct.pack('<Q', int(calcCRC, base=16))
        print ('CALC CRC HEX and byte: ')

        #print(calcCRC)
        #print (CRCtoSend)
        #send only 2 bytes
        cmd_byteData += CRCtoSend[0:2]
        
        # Write to serial port
        # TO DO put in separate function
        if (len(bytearray(cmd_byteData))) == 22:
            #self.ser.write_timeout = (0.30)
            try:
                i = 0
                
                for i in range(len(cmd_byteData)):
                    self.ser.write(cmd_byteData[i:i+1])
                # END DEBUG
                                #self.ser.write(cmd_byteData)
                # DEBUG
                # print('length of CMD Pkt:')
                # print (len(bytearray(cmd_byteData)))
                print ("Packet Written:")
                print(''.join(r'\x'+hex(letter)[2:] for letter in cmd_byteData))
                print("Sent back SEQ and CRC: ")
                print (int.from_bytes(cmd_byteData[0:2], byteorder='little'))
                print (int.from_bytes(cmd_byteData[20:], byteorder='little'))
                self.ser.reset_output_buffer()
                return True
                    
            except serial.SerialException:
                print('Serial write error')
                return False
        else:
            print ('Data packet too long')

        

    def run(self) -> None:
        self.done = False
        
        if self.init_serial():
            sleep(1)
            print ('Serial Init Successful')
        else:
            print ('Serial Initialization failed')
            # When the alarm infrastructure is done this would trigger an alarm
            return
        self.process_SerialData()
       