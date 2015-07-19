# Open a serial connection to a meteostick, reset and initialise th device
# then packetise the output for processing
#
# (C) Fergus Duncan 2015
#

import sys
import time
import serial

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
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.open()
ser.isOpen()

# Reset the meteostick so we know what state it is in
# Current implementation produces some text and finally produces a ? character
# which indicates it's ready to roll

ser.write('r\n') # This is the reset command

# Wait until we see the ? character
ready = False
while ready == False :
        time.sleep(0.1)
        while ser.inWaiting() > 0:
            data=ser.read(1)
            if data == '?' :
            	ready = True
	    sys.stdout.write(data)

time.sleep(0.2)
ser.flushInput()

# Set device to listen to transmitter 1
# Then discard any serial input from the device
ser.write('t1\r')
time.sleep(0.2)
response = ser.read(ser.inWaiting())
print response
ser.flushInput()

# Set device to filter out transmissions from anything other than transmitter 1
# Then discard any serial input from the device
ser.write('f1\r')
time.sleep(0.2)
response = ser.read(ser.inWaiting())
print response
ser.flushInput()

# Set device to produce raw data
# Then discard any serial input from the device
ser.write('o0\r')
time.sleep(0.2)
response = ser.read(ser.inWaiting())
print response
ser.flushInput()

# Set device to listen on european frequencies (868MHz)
# Then discard any serial input from the device
ser.write('m1\r')
time.sleep(0.2)
response = ser.read(ser.inWaiting())
print response
ser.flushInput()

# Now loop creating data packets
string = ''
started = False
while True :
        time.sleep(0.1)
        while ser.inWaiting() > 0:
            data=ser.read(1)
	    #sys.stdout.write(data)
	    #print data, data.encode('hex')
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
