 
# Copyright 2020 LifeMech  Inc
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, 
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
# is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


import json
import logging
import random
import time
from threading import Thread, Lock
import serial
import sys
from time import sleep
from datetime import datetime
import codecs
import struct
import crc16
import os
import glob

from utils.params import Params
from utils.settings import Settings
from utils.serial_watchdog import Watchdog
from utils.in_packet import InPacket
from utils.out_packet import OutPacket
from utils.crc import CRC
from utils.units import Units
from PyQt5.QtCore import QThread, pyqtSignal


class CommsLink(QThread):
    new_params = pyqtSignal(Params)
    new_alarms = pyqtSignal(int)
    lost_comms_signal = pyqtSignal()

    def __init__(self, port: str) -> None:
        QThread.__init__(self)
        self.logger = logging.getLogger()
        self.settings = Settings()
        self.settings_lock = Lock()
        self.packet_version = 4
        self.BAUD = 500000
        self.PORT = port
        self.SER_TIMEOUT = 0.065
        self.SER_WRITE_TIMEOUT = None
        self.SER_INTER_TIMEOUT = None
        self.SER_MAX_REREADS = 30
        self.ser = 0
        self.FALLBACK_IE = float(1 / 1.5)
        self.rxState=0
        self.lastSeq=-1
        self.alarmbits = 0
        self.ackbits = 0
        self.enable_calibration = False
        #statistics
        self.statSeqError=0
        self.statPacketRxCntOk=0
        self.statPacketRxCntCrcFail=0
        self.statPacketRxCntLenFail=0
        self.statPacketRxCntHeaderFail=0
        self.statPacketTxCntOk=0
        self.statPacketTxFailCnt=0
        self.statPrintCnt=0
        self.sequenceNoTx=0
        self.dirName='/home/pi/logs'
        if not os.path.exists(self.dirName):
            os.makedirs(self.dirName)
        dateStr=datetime.now().isoformat(timespec='minutes')
        self.binaryLogFile=open(str(self.dirName)+"/["+dateStr+"] binary.log","wb+")
        self.textLogFile=open(str(self.dirName)+"/["+dateStr+"] text.log","wb+")
        

    def update_settings(self, settings_dict: dict) -> None:
        self.settings_lock.acquire()
        self.settings.from_dict(settings_dict)
        self.settings_lock.release()
        self.logger.debug("Got updated settings from UI")
        self.logger.debug(self.settings.to_JSON())

    def ready_to_calibrate(self):
        self.enable_calibration = True

    def ready_to_ventilate(self):
        self.enable_calibration = False

    def set_alarm_ackbits(self, ackbits: int) -> None:
        self.logger.debug("Commslink got ackbits :" + str(ackbits))
        # If an alarm is not active, do not ack it
        self.ackbits = ackbits & self.alarmbits

    #receive state machine per byte. Calls processPacket for each successful packet
    def handleRxByte(self, byte) -> None:
        if self.rxState == 0:
            if byte== 0x26: #check for first sync byte
                self.rxState=1
        elif self.rxState == 1:
            if byte== 0x56: #check for 2nd sync byte
                self.rxState=2
            elif byte!= 0x26: #make sure to catch S1S1S2S3 sync byte combination
                self.rxState=0
                self.statPacketRxCntHeaderFail+=1
        elif self.rxState == 2:
            if byte== 0x7E: #check for 3rd sync byte
                self.rxState=3
            else:
                self.rxState=0
                self.statPacketRxCntHeaderFail+=1
        elif self.rxState==3:
            self.crcCalc = crc16.crc16xmodem(byte.to_bytes(1, 'little'), 0xffff) #init CRC with 0xffff
            self.seqNum=byte    #lower byte of seq no
            self.rxState=4
        elif self.rxState==4:
            self.crcCalc = crc16.crc16xmodem(byte.to_bytes(1, 'little'), self.crcCalc)
            self.seqNum+=byte<<8 #high byte of seq no
            self.rxState=5
        elif self.rxState==5:
            self.crcCalc = crc16.crc16xmodem(byte.to_bytes(1, 'little'), self.crcCalc)
            if byte!=4: #check protocol version
                self.rxState=0
            else:
                self.rxState=6
        elif self.rxState==6:
            self.crcCalc = crc16.crc16xmodem(byte.to_bytes(1, 'little'), self.crcCalc)
            self.msgType=byte #store packetType
            self.rxState=7
            self.rxCnt=0
            self.rxData=bytearray()
        elif self.rxState==7:
            self.crcCalc = crc16.crc16xmodem(byte.to_bytes(1, 'little'), self.crcCalc)
            self.packetLen=byte #store length
            if (self.packetLen<=128): #128 is max
                self.rxState=8
            else:
                self.statPacketRxCntLenFail+=1
                self.rxState=0
        elif self.rxState==8:
            self.crcCalc = crc16.crc16xmodem(byte.to_bytes(1, 'little'), self.crcCalc)
            self.rxData.append(byte) #save data
            self.rxCnt+=1
            if self.rxCnt==self.packetLen:
                self.rxState=9
        elif self.rxState==9:
            self.recCrc=byte #low byte crc
            self.rxState=10
        elif self.rxState==10:
            self.recCrc|=byte<<8 #high byte crc
            if self.recCrc==self.crcCalc: #check crc
                self.statPacketRxCntOk+=1
                self.processPacket(self.rxData,self.msgType,self.seqNum)
            else:
                self.logger.debug("Got packet with wrong CRC! Rec: "+str(self.recCrc)+" Calc: "+str(self.crcCalc))
                self.statPacketRxCntCrcFail+=1
            self.rxState=0 #restart state machine
        
    def get_bytes_from_serial(self) -> str:
        byteData = b''
        byteData = self.read_all(self.ser)
        return byteData

    def create_cmd_pkt(self):
        self.settings_lock.acquire()

        self.cmd_pkt.data['mode_value'] = self.settings.mode
        self.cmd_pkt.data['command'] = self.cmd_pkt.pack_command(self.settings.run_state, 0, 
            self.settings.should_shut_down, self.enable_calibration)
        self.cmd_pkt.data['respiratory_rate_set'] = self.settings.resp_rate
        self.cmd_pkt.data['tidal_volume_set'] = Units.ml_to_ecu(
            self.settings.tv)

        # The UI selects the I:E ratio from an enumeration.
        # Get the fractional value from the enumeration and convert to fixed point.
        # If the lookup somehow fails, set I:E to a safe fallback value. 
        ie_fraction = self.settings.ie_ratio_switcher.get(self.settings.ie_ratio_enum, self.FALLBACK_IE)
        ie_ratio_fixed = self.cmd_pkt.ie_fraction_to_fixed(ie_fraction)
        self.cmd_pkt.data['ie_ratio_set'] = ie_ratio_fixed
        
        self.cmd_pkt.data['alarm_bits'] = self.ackbits

        self.cmd_pkt.data['high_pressure_limit_set'] =  Units.cmh2o_to_ecu(self.settings.high_pressure_limit)
        self.cmd_pkt.data['low_pressure_limit_set'] =  Units.cmh2o_to_ecu(self.settings.low_pressure_limit)
        self.cmd_pkt.data['high_volume_limit_set'] =  Units.ml_to_ecu(self.settings.high_volume_limit)
        self.cmd_pkt.data['low_volume_limit_set'] =  Units.ml_to_ecu(self.settings.low_volume_limit)
        self.cmd_pkt.data['high_respiratory_rate_limit_set'] = self.settings.high_resp_rate_limit
        self.cmd_pkt.data['low_respiratory_rate_limit_set'] = self.settings.low_resp_rate_limit

        self.settings_lock.release()

    def processPacket(self, byteData, packetType, sequenceNo):
        #handle public data packet
        if ((self.lastSeq+1!=sequenceNo) and (self.lastSeq!=-1)):
                self.logger.debug('Error in sequence -> likely packet drop')
                self.statSeqError+=1

        self.lastSeq=sequenceNo

        if packetType==0x01:
            inpkt = {}
            inpkt['type'] = "inpkt"
            inpkt['bytes'] = str(byteData)
            self.logger.log(25, json.dumps(inpkt))
            self.in_pkt.from_bytes(byteData)

            self.alarmbits = self.in_pkt.data["alarm_bits"]

            self.new_params.emit(self.in_pkt.to_params(sequenceNo))
            self.new_alarms.emit(self.alarmbits)
       
            self.create_cmd_pkt()
            cmd_byteData = self.cmd_pkt.to_bytes()
            outpkt = {}
            outpkt['type'] = "outpkt"
            outpkt['bytes'] = str(cmd_byteData)
            self.logger.log(25, json.dumps(outpkt))
            self.sendPkts(cmd_byteData)

            
        elif packetType==0x80:
            self.textLogFile.write(byteData)
            self.textLogFile.flush()


    #This function processes the serial data from Arduino and sends ACK
    def process_SerialData(self) -> None:
        params = Params()
        params_str = params.to_JSON()
        params_dict = json.loads(params_str)
        
        self.in_pkt = InPacket()
        self.cmd_pkt = OutPacket()
        self.crc = CRC()

        self.ser.reset_input_buffer()

        while True:
            byteData = self.get_bytes_from_serial()
            self.binaryLogFile.write(byteData)
            self.binaryLogFile.flush()
            fileSize=self.binaryLogFile.tell()
            #max 8Mbyte per file so it fit's in one e-mail. Assumes that binaryFile larger than textLogFile
            if (fileSize>(8*1024*1024)): 
                self.binaryLogFile.close()
                self.textLogFile.close()
                dateStr=datetime.now().isoformat(timespec='minutes')
                self.binaryLogFile=open(str(self.dirName)+"/["+dateStr+"] binary.log","wb+")
                self.textLogFile=open(str(self.dirName)+"/["+dateStr+"] text.log","wb+")

            for byte in byteData:
                self.handleRxByte(byte)
            #do some statistics logging regularly
            self.statPrintCnt+=1
            if (self.statPrintCnt==200):
                self.logger.warning('Serial TX-Stat: OK:' + str(self.statPacketTxCntOk)+' Fail:'+str(self.statPacketTxFailCnt))
                self.logger.warning('Serial RX-Stat: OK:' + str(self.statPacketRxCntOk)+' Fail (CRC):'+str(self.statPacketRxCntCrcFail)+' (Hdr):'+str(self.statPacketRxCntHeaderFail)+'Len:'+str(self.statPacketRxCntLenFail)+' Fail(Seq):'+str(self.statSeqError))
                self.statPrintCnt=0
            sleep(0.01) #check every 10ms for new data packets

    def init_serial(self) -> False:

        self.ser = serial.Serial()
        self.ser.baudrate = self.BAUD
        self.ser.port = self.PORT
        self.ser.timeout = self.SER_TIMEOUT
        self.ser.write_timeout = self.SER_WRITE_TIMEOUT

        try:
            if self.ser.is_open:
                self.ser.close()
                self.logger.info("Disconnected current connection.")
                return False
            else:
                self.ser.open()
                self.logger.info("Successfully connected to port %r." %
                                 self.ser.port)
                return True
        except serial.SerialException:
            return False

    #read a chunk of data
    def read_all(self, port, chunk_size=512):
        """Read all characters on the serial port and return them."""
        if not port.isOpen():
            raise SerialException('Serial is diconnected')
        if not port.timeout:
            raise TypeError('Port needs to have a timeout set!')

        read_buffer = b''

        read_buffer+= port.read(size=chunk_size)

        return read_buffer

    #send a packet
    def sendPkts(self, cmd_byteData: bytes) -> None:
        # Write to serial port
        # TO DO put in separate function

        try:
            
            self.ser.write(bytes([ 0x26,0x56,0x7e ]))
            self.ser.write(self.sequenceNoTx.to_bytes(2,'little'))
            txCrc=crc16.crc16xmodem(self.sequenceNoTx.to_bytes(2,'little'), 0xFFFF)
            self.ser.write(bytes([ 4 ]))
            txCrc=crc16.crc16xmodem(bytes([ 4 ]), txCrc)
            self.ser.write(bytes([ 0x02 ]))
            txCrc=crc16.crc16xmodem(bytes([ 0x02 ]), txCrc)
            self.ser.write(len(cmd_byteData).to_bytes(1,'little'))
            txCrc=crc16.crc16xmodem(len(cmd_byteData).to_bytes(1,'little'), txCrc)

            for i in range(len(cmd_byteData)):
                txCrc=crc16.crc16xmodem(cmd_byteData[i:i + 1], txCrc)
                self.ser.write(cmd_byteData[i:i + 1])
            self.ser.write(txCrc.to_bytes(2,'little'))

            self.logger.debug("Packet Written:")
            self.logger.debug("Sent back SEQ and CRC: ")
            self.logger.debug(self.sequenceNoTx)
            self.logger.debug(txCrc)
            self.statPacketTxCntOk+=1
            self.sequenceNoTx = (self.sequenceNoTx + 1) & 0xFFFF
            return True

        except serial.SerialException:
            self.statPacketTxFailCnt+=1
            self.logger.exception('Serial write error')
            return False

    def run(self) -> None:
        if self.init_serial():
            sleep(1)
            self.logger.debug('Serial Init Successful')
        else:
            self.logger.error('Serial Initialization failed')
            # Signal the UI to display and sound an alarm
            #self.lost_comms_signal.emit()
            return
        
        try:
            self.process_SerialData()
        except:
            self.logger.debug("Received serial exception")
        