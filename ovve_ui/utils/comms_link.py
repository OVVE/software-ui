import json
import logging
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
from utils.crc import CRC
from utils.units import Units
from PyQt5.QtCore import QThread, pyqtSignal


class CommsLink(QThread):
    new_params = pyqtSignal(Params)
    new_alarms = pyqtSignal(int)

    def __init__(self, port: str) -> None:
        QThread.__init__(self)
        self.logger = logging.getLogger()
        self.settings = Settings()
        self.settings_lock = Lock()
        self.packet_version = 1
        self.BAUD = 38400
        self.PORT = port
        self.SER_TIMEOUT = 0.065
        self.SER_WRITE_TIMEOUT = 0.03
        self.SER_INTER_TIMEOUT = 0.01
        self.SER_MAX_REREADS = 30
        self.ser = 0
        self.FALLBACK_IE = float(1 / 1.5)
        self.alarmbits = 0
        self.ackbits = 0

    def update_settings(self, settings_dict: dict) -> None:
        self.settings_lock.acquire()
        self.settings.from_dict(settings_dict)
        self.settings_lock.release()
        self.logger.debug("Got updated settings from UI")
        self.logger.debug(self.settings.to_JSON())

    def set_alarm_ackbits(self, ackbits: int) -> None:
        self.logger.debug("Commslink got ackbits :" + str(ackbits))
        # If an alarm is not active, do not ack it
        self.ackbits = ackbits & self.alarmbits

    def get_bytes_from_serial(self) -> str:
        byteData = b''
        rereadCount = 0
        while len(bytearray(
                byteData)) != 56 and rereadCount < self.SER_MAX_REREADS:
            byteData = self.read_all(self.ser, 56)
            if len(bytearray(byteData)) < 56:
                self.logger.debug("reread " + str(rereadCount))
            rereadCount += 1

        self.ser.flush()
        return byteData

    def check_sequence(self, byteData) -> bool:
        if byteData[0:2] == b'\x00\x00':
            prevSeq = -1
            currentSeq = int.from_bytes(byteData[0:2], byteorder='little')
        else:
            prevSeq = (int.from_bytes(byteData[0:2], byteorder='little') - 1)
            currentSeq = int.from_bytes(byteData[0:2], byteorder='little')

        if currentSeq != (prevSeq + 1):
            self.logger.warning("Sequence Error! cur:" + str(self.currentSeq) +
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
        self.cmd_pkt.data['tidal_volume_set'] = Units.ml_to_ecu(
            self.settings.tv)

        # The UI selects the I:E ratio from an enumeration.
        # Get the fractional value from the enumeration and convert to fixed point.
        # If the lookup somehow fails, set I:E to a safe fallback value. 
        ie_fraction = self.settings.ie_ratio_switcher.get(self.settings.ie_ratio_enum, self.FALLBACK_IE)
        ie_ratio_fixed = self.cmd_pkt.ie_fraction_to_fixed(ie_fraction)
        self.cmd_pkt.data['ie_ratio_set'] = ie_ratio_fixed
        
        self.cmd_pkt.data['alarm_bits'] = self.ackbits

        self.settings_lock.release()


    #This function processes the serial data from Arduino and sends ACK
    def process_SerialData(self) -> None:
        params = Params()
        params_str = params.to_JSON()
        params_dict = json.loads(params_str)
        error_count = 0
        validData = False

        self.in_pkt = InPacket()
        self.cmd_pkt = OutPacket()
        self.crc = CRC()

        self.ser.reset_input_buffer()

        validData = False
        valid_pkt_count = 0

        while True:
            byteData = self.get_bytes_from_serial()
            seqOK = self.check_sequence(byteData)
            crcOK = self.crc.check_crc(byteData)

            inpkt = {}
            inpkt['type'] = "inpkt"
            inpkt['bytes'] = str(byteData)
            
            if crcOK and seqOK:
                # Log raw packet data at a level betwen INFO and WARNING so that
                # we can log only raw packets in production
                self.logger.log(25, json.dumps(inpkt))
                self.in_pkt.from_bytes(byteData)
                self.alarmbits = self.in_pkt.data["alarm_bits"]

                self.new_params.emit(self.in_pkt.to_params())
                self.new_alarms.emit(self.alarmbits)

                self.create_cmd_pkt()  
                
                cmd_byteData = self.cmd_pkt.to_bytes()

                outpkt = {}
                outpkt['type'] = "outpkt"
                outpkt['bytes'] = str(cmd_byteData)
                self.logger.log(25, json.dumps(outpkt))
                self.sendPkts(cmd_byteData)
                valid_pkt_count += 1
            else:
                self.logger.warning("BAD PACKET: " + json.dumps(inpkt))
                error_count += 1

            self.logger.debug('Dropped packets count ' + str(error_count))
            self.logger.debug('Valid packets count ' + str(valid_pkt_count))

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

    def sendPkts(self, cmd_byteData: bytes) -> None:
        # Write to serial port
        # TO DO put in separate function
        if (len(bytearray(cmd_byteData))) == 34:
            #self.ser.write_timeout = (0.30)
            try:
                i = 0

                for i in range(len(cmd_byteData)):
                    self.ser.write(cmd_byteData[i:i + 1])

                self.logger.debug("Packet Written:")
                self.logger.debug(''.join(r'\x' + hex(letter)[2:]
                                          for letter in cmd_byteData))
                self.logger.debug("Sent back SEQ and CRC: ")
                self.logger.debug(
                    int.from_bytes(cmd_byteData[0:2], byteorder='little'))
                self.logger.debug(
                    int.from_bytes(cmd_byteData[32:], byteorder='little'))
                self.ser.reset_output_buffer()
                return True

            except serial.SerialException:
                self.logger.exception('Serial write error')
                return False
        else:
            self.logger.warning('Data packet too long')

    def run(self) -> None:
        if self.init_serial():
            sleep(1)
            self.logger.debug('Serial Init Successful')
        else:
            self.logger.error('Serial Initialization failed')
            # When the alarm infrastructure is done this would trigger an alarm
            return
        self.process_SerialData()
