"""
MIT License

Copyright (c) 2017 Jose Navarro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Python script to send data using the Microchip RN2XX3 LoRa module on a Raspberry Pi Zero LoRa hat. 
To free the Mini UART open a terminal enter the command:

$sudo raspi-config 

Go to option 5 Interfacing Options
Then option P6 Serial
Would you like a login shell to be accesible over serial? Say No
Would you like the serial port hardware to be enabled?  Say Yes
Select Ok then Finish. 
Reboot

Python script use example:
$sudo python lora_send_RPi_LoRaHat.py 'text to send'
"""

import time
import sys
import serial

ser = serial.Serial()
ser.port = "/dev/ttyAMA0"
ser.baudrate = 57600
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.timeout = 8
ser.xonxoff = False
ser.rtscts = False
ser.dsrdtr = False
ser.writeTimeout = 0

try:
    ser.open()
except Exception, e:
    print "error open serial port: " + str(e)
    exit()

time.sleep(1)

def module_setup(command):
    ser.write(command + '\r\n')
    response = ser.readline().strip()
    print response
    time.sleep(0.5)

module_setup('sys reset')
time.sleep(0.5)
module_setup('mac set appeui 0000000000000000’) //Replace zeroes with your appeui
module_setup('mac set appkey 00000000000000000000000000000000’) //Replace zeroes with your appkey
module_setup('radio set crc on')
module_setup('mac set dr 0')
module_setup('mac join otaa')
join_response = ser.readline().strip()
if join_response == 'accepted':
    print "Connected to gateway", join_response
else:
    print "Not joined - ", join_response

data=sys.argv[1]
data.encode("hex")
data1 = data.encode("hex")
print data1

time.sleep(5)
ser.write('mac tx uncnf 1 %s'%data1 + '\r\n')
tx_command_response = ser.readline().strip()
if tx_command_response == 'ok':
    print "tx command accepted", tx_command_response
else:
    print "tx command error - ", tx_command_response
tx_response = ser.readline().strip()
if tx_response == 'mac_tx_ok':
    print "tx success", tx_response
else:
    print "tx error - ", tx_response
