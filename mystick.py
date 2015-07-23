# Open a serial connection to a meteostick, reset and initialise th device
# then packetise the output for processing
#
# (C) Fergus Duncan 2015
#

import sys
import time
import serial
import threading

def processIstring(string) :
    fields = string.strip().split()
    byte0 = int(fields[2],16)
    byte1 = int(fields[3],16)
    byte2 = int(fields[4],16)
    byte3 = int(fields[5],16)
    byte4 = int(fields[6],16)
    byte5 = int(fields[7],16)
    byte6 = int(fields[8],16)
    byte7 = int(fields[9],16)

def processBstring(string) :
    fields = string.strip().split()

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

def getSerialData(lock) :
    ser.open()
    ser.isOpen()

    string = ''
    started = False
    while True :
        time.sleep(0.1)
        while ser.inWaiting() > 0:
            data=ser.read(1)
	    if started == False :
   		if (data == 'I') or (data == 'B') :
     		    started = True
		    string += data
	    else :
            	if (data == '\r') :
		    print string
		    started = False
		    if string[0] == 'I' :
			processIstring(string)
                    elif string[0] == 'B' :
			processBstring(string)
                    string = ''
		else :
		    string += data


lock = threading.Lock()
thread = threading.Thread(target=getSerialData,args=(lock,))
thread.daemon = True
thread.start()

while True :
    time.sleep(1)
