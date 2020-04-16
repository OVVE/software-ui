import json
import random
import time
from threading import Thread, Lock
import serial
import sys
from time import sleep
import binascii
import codecs
import struct

from utils.params import Params
from utils.settings import Settings
from utils.serial_watchdog import Watchdog
from utils.in_packet import InPacket
from utils.out_packet import OutPacket
from utils.logger import Logger

from PyQt5.QtCore import QThread, pyqtSignal


class CommsLink(QThread):
    new_params = pyqtSignal(Params)
    new_alarms = pyqtSignal(dict)

    def __init__(self, logger: Logger) -> None:
        QThread.__init__(self)
        self.logger = Logger
        self.settings = Settings()
        self.settings_lock = Lock()
        self.seqnum = 0
        self.packet_version = 1
        self.BAUD = 38400
        self.PORT = "/dev/ttyACM0"
        self.SER_TIMEOUT = 0.055
        self.ser = 0
        self.crcFailCnt = 0
        self.setting_lock = Lock()
        self.debug = True
        

    def update_settings(self, settings_dict: dict) -> None:
        self.settings_lock.acquire()
        self.settings.from_dict(settings_dict)
        self.settings_lock.release()
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
        ValidPkt = 0

        self.in_pkt = InPacket()
        self.out_pkt = OutPacket()

        self.ser.reset_input_buffer()
        byteData = b''
        
        while True:    
            byteData = self.read_all(self.ser, 70)
            if len(bytearray(byteData)) != 70:
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
            # END DEBUG
            currentSeq = int.from_bytes(byteData[0:2], byteorder='little')                                  
            if  currentSeq != 0 and currentSeq != ( prevSeq + 1) :
                print ("There appears to be Sequence Error")
                print (currentSeq)
                print (prevSeq)
            prevSeq = currentSeq

            crcOK = self.crc.checkCrc(byteData[68:])
            if not crcOK:
                print ("CRC check failed")
                self.crcFailCnt += self.crcFailCnt
                error_count = error_count + 1
                validData = False
                if self.debug:
                    print (rcvdCRC)
                    print (calcRcvCRC)
                    print ('Dropped packets count ' + str(error_count))
                    print ('Valid packets count ' + str(ValidPkt))
            else:
                validData = True
                self.in_pkt.from_bytes(byteData)
                if self.debug:
                    print ('Received SEQ and CRC:')
                    print (in_pkt['sequence_count'])
                    print (in_pkt['crc'])

            # Watchdog to be implemented later
            # wd = Watchdog(100)
            # try:

            
            # Lock to prevent settings from being written in the middle of
            # creating the packet.
            self.settings_lock.acquire()
            # get the updates from settings TODO: Make this event driven and only when callbackis called
            self.cmd_pkt.data['sequence_count'] = self.in_pkt.data['sequence_count']
            self.cmd_pkt.data['mode_value'] = self.settings.mode
            self.cmd_pkt.data['respiratory_rate_set'] = self.settings.resp_rate
            self.cmd_pkt.data['tidal_volume_set'] = self.settings.tv
            self.cmd_pkt.data['ie_ratio_set'] = self.settings.ie_ratio
            self.settings_lock.release()

            cmd_byteData = self.cmd_pkt.to_bytes()

            # Write to serial port
            # TO DO put in separate function
            if (len(bytearray(cmd_byteData))) == 22:
                try:
                    self.ser.write(cmd_byteData)
                    self.ser.reset_output_buffer()
                except:
                    print('Serial write error')
            else:
                print ('Data packet too long')
   
            if debug:
                # DEBUG
                # print('length of CMD Pkt:')
                # print (len(bytearray(cmd_byteData)))
                # print ("Packet Written:")
                # print(''.join(r'\x'+hex(letter)[2:] for letter in cmd_byteData))
                print("Sent back SEQ and CRC: ")
                print (int.from_bytes(cmd_byteData[0:2], byteorder='little'))
                print (int.from_bytes(cmd_byteData[20:], byteorder='little'))
                # END DEBUG

            #Update dict only if there is valid data
            if validData:
                # any settings set will not retunr correctly yet until Arduino sets set values correctly
                # We can use the settings values like in simulator if so desired or maybe compare them
                # RE: Run_state, we still need to implment getting this from Arduino. Currently I am just getting zero
                # When done, this will MSB off in_pkt['mode_value']
                params = self.in_pkt.to_params()
                params.run_state = self.settings.run_state
                self.new_params.emit(params)

           
    def init_serial(self) -> False:

        self.ser = serial.Serial()
        self.ser.baudrate = self.BAUD
        self.ser.port = self.PORT 
        self.ser.timeout = self.SER_TIMEOUT
        
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
        port.reset_input_buffer()
        return read_buffer


    def run(self) -> None:
        if self.init_serial():
            print ('Serial Init Successful')
        else:
            print ('Serial Initialization failed')
            # When the alarm infrastructure is done this would trigger an alarm
            return
        self.process_SerialData()
       