 
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


import serial
import sys
from time import sleep
import binascii
import crc16
import codecs

BAUD = 38400
PORT = "/dev/ttyACM0"
SER_TIMEOUT = 0.055


#Global Variables
ser = 0
dicA = {'ver': '', 'seq': '' }

#Function to Initialize the Serial Port
def init_serial():
    
    global ser          #Must be declared in Each Function
    ser = serial.Serial()
    ser.baudrate = BAUD
    ser.port = PORT 
    #a little less than polling spped from arduino
    ser.timeout = SER_TIMEOUT
    ser.open()          #Opens SerialPort

    # print port open or closed
    if ser.isOpen():
        print ('Open: ' + ser.portstr)
    sleep(1)    
#Function Ends Here
        

#Call the Serial Initilization Function, Main Program Starts from here
init_serial()

def crccitt(hex_string):
    byte_seq = binascii.unhexlify(hex_string)
    crc = crc16.crc16xmodem(byte_seq, 0xffff)
    return '{:04X}'.format(crc & 0xffff)

def read_all(port, chunk_size=200):
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

#ser.flush()
count = 0
def send_Data():
    global ser     
    ser.reset_input_buffer()
    cmd_byteData = b""
    testData = [ 0x82, 0x00, 0x3A ]
    endian = "little"
    error_count = 0
    while True:
        cmd_byteData = b""
        testData = b'\x82\x00\x3A'
        cmd_byteData += bytes(testData[0].to_bytes(1, endian))
        cmd_byteData += bytes(testData[1].to_bytes(1, endian))
        cmd_byteData += bytes(testData[2].to_bytes(1, endian))
        calcCRC = crccitt(cmd_byteData.hex())
        print ('CALC CRC HEX and int: ')
        print(calcCRC)
        print(int(calcCRC, 16))
        cmd_byteData += bytes.fromhex(calcCRC)

        ser.write(cmd_byteData)
        
        print("Sent back SEQ and CRC: ")
        
        print (int.from_bytes(cmd_byteData[1:3], byteorder='little'))
        print (int.from_bytes(cmd_byteData[21:], byteorder='big'))
        sleep(0.1)
if __name__ == '__main__':
    send_Data()



    
    
