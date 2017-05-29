"""
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

Jose Navarro
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
