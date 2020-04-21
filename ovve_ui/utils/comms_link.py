import json
import random
import time
from threading import Thread, Lock
import serial
import sys
from time import sleep
import codecs
import struct

from utils.params import Params
from utils.settings import Settings
from utils.serial_watchdog import Watchdog
from utils.in_packet import InPacket
from utils.out_packet import OutPacket
from utils.logger import Logger
from utils.crc import CRC
from PyQt5.QtCore import QThread, pyqtSignal


class CommsLink(QThread):
    new_params = pyqtSignal(Params)
    new_alarms = pyqtSignal(dict)

    def __init__(self, logger: Logger) -> None:
        QThread.__init__(self)
        self.logger = logger
        self.settings = Settings()
        self.settings_lock = Lock()
        self.packet_version = 1
        self.BAUD = 38400
        self.PORT = "/dev/ttyUSB0"
        self.SER_TIMEOUT = 0.065
        self.SER_WRITE_TIMEOUT = 0.03
        self.SER_INTER_TIMEOUT = 0.01
        self.SER_MAX_REREADS = 30
        self.ser = 0
        self.debug = False

    def update_settings(self, settings_dict: dict) -> None:
        self.settings_lock.acquire()
        self.settings.from_dict(settings_dict)
        self.settings_lock.release()
        if self.debug:
            self.logger.log("debug", "Got updated settings from UI")
            self.logger.log("debug", self.settings.to_JSON())

    def get_bytes_from_serial(self) -> str:
        byteData = b''
        rereadCount = 0
        while len(bytearray(
                byteData)) != 70 and rereadCount < self.SER_MAX_REREADS:
            byteData = self.read_all(self.ser, 70)
            if len(bytearray(byteData)) < 70 and self.debug:
                self.logger.log("debug", "reread " + str(rereadCount))
            rereadCount += 1

        self.ser.flush()

        if self.debug:
            self.logger.log("debug", len(bytearray(byteData)))

        return byteData

    def check_sequence(self, byteData) -> bool:
        if byteData[0:2] == b'\x00\x00':
            prevSeq = -1
            currentSeq = int.from_bytes(byteData[0:2], byteorder='little')
        else:
            prevSeq = (int.from_bytes(byteData[0:2], byteorder='little') - 1)
            currentSeq = int.from_bytes(byteData[0:2], byteorder='little')

        if currentSeq != (prevSeq + 1):
            if self.debug:
                self.logger.log(
                    "debug", "Sequence Error! cur:" + str(self.currentSeq) +
                    " prev:" + str(self.prevSeq))
            seqOK = False
        else:
            seqOK = True

        return seqOK

    def create_cmd_pkt(self):
        self.settings_lock.acquire()

        self.cmd_pkt.data['mode_value'] = self.cmd_pkt.calculate_mode(
            self.settings.mode, self.settings.run_state)
        self.cmd_pkt.data['sequence_count'] = self.in_pkt.data[
            'sequence_count']
        self.cmd_pkt.data['respiratory_rate_set'] = self.settings.resp_rate
        self.cmd_pkt.data['tidal_volume_set'] = self.settings.tv
        self.cmd_pkt.data['ie_ratio_set'] = self.settings.ie_ratio

        self.settings_lock.release()

    #This function processes the serial data from Arduino and sends ACK
    def process_SerialData(self) -> None:
        params = Params()
        params_str = params.to_JSON()
        params_dict = json.loads(params_str)
        error_count = 0
        validData = False

        self.in_pkt = InPacket(self.logger)
        self.cmd_pkt = OutPacket(self.logger)
        self.crc = CRC(self.logger)

        self.ser.reset_input_buffer()

        validData = False
        valid_pkt_count = 0

        while True:
            byteData = self.get_bytes_from_serial()
            seqOK = self.check_sequence(byteData)
            crcOK = self.crc.check_crc(byteData)

            if crcOK and seqOK:
                self.in_pkt.from_bytes(byteData)
                self.new_params.emit(self.in_pkt.to_params())

                self.create_cmd_pkt()
                self.sendPkts()
                valid_pkt_count += 1
            else:
                error_count += 1

            if self.debug:
                self.logger.log("debug",
                                'Dropped packets count ' + str(error_count))
                self.logger.log("debug",
                                'Valid packets count ' + str(valid_pkt_count))

    def init_serial(self) -> False:

        self.ser = serial.Serial()
        self.ser.baudrate = self.BAUD
        self.ser.port = self.PORT
        self.ser.timeout = self.SER_TIMEOUT
        self.ser.write_timeout = self.SER_WRITE_TIMEOUT

        try:

            if self.ser == None:
                self.ser.open()
                self.logger.log(
                    "debug",
                    "Successfully connected to port %r." % self.ser.port)

                return True
            else:
                if self.ser.isOpen():
                    self.ser.close()
                    self.logger.log("debug",
                                    "Disconnected current connection.")
                    return False
                else:
                    self.ser.open()
                    self.logger.log("debug",
                                    "Connected to port %r." % self.ser.port)
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
        #port.reset_input_buffer()
        return read_buffer

    def sendPkts(self):

        cmd_byteData = self.cmd_pkt.to_bytes()

        # Write to serial port
        # TO DO put in separate function
        if (len(bytearray(cmd_byteData))) == 22:
            #self.ser.write_timeout = (0.30)
            try:
                i = 0

                for i in range(len(cmd_byteData)):
                    self.ser.write(cmd_byteData[i:i + 1])

                if self.debug:
                    self.logger.log("debug", "Packet Written:")
                    self.logger.log(
                        "debug", ''.join(r'\x' + hex(letter)[2:]
                                         for letter in cmd_byteData))
                    self.logger.log("debug", "Sent back SEQ and CRC: ")
                    self.logger.log(
                        "debug",
                        int.from_bytes(cmd_byteData[0:2], byteorder='little'))
                    self.logger.log(
                        "debug",
                        int.from_bytes(cmd_byteData[20:], byteorder='little'))
                self.ser.reset_output_buffer()
                return True

            except serial.SerialException:
                self.logger.log("debug", 'Serial write error')
                return False
        else:
            self.logger.log("debug", 'Data packet too long')

    def run(self) -> None:
        if self.init_serial():
            sleep(1)
            self.logger.log("debug", 'Serial Init Successful')
        else:
            self.logger.log("debug", 'Serial Initialization failed')
            # When the alarm infrastructure is done this would trigger an alarm
            return
        self.process_SerialData()
