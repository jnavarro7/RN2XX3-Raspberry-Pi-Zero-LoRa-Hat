# Raspberry Pi Zero LoRA hat based on the RN2903 module. 

Python script to send data from a Microchip RN2903 915MHz LoRa Radio module to a gateway, connection done using OTAA.
This establishes a connection to a LoRa Gateway and sends a message to it which can then be parsed in the gateway.  I commonly use Node Red to connect to a Twitter account and display data. 

## UART

The UART bus is commonly exposed in Linux as

    /dev/ttyAMA0

## Python Script

The script stablishes the connection with the Microchip RN2XX3 module via UART at a 57600 baud rate. Transmit data to it and reads its response.

## Usage

    sudo python lora_send_RPi_LoRaHat.py 'text to send'

### Hardware

Hardware design files located in the "hardware" directory.

![alt tag](/pictures/1.png)

![alt tag](/pictures/2.png)

![alt tag](/pictures/3.png)

![alt tag](/pictures/4.png)