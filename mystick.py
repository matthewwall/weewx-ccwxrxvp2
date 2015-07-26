# Open a serial connection to a meteostick, reset and initialise th device
# then packetise the output for processing
#
# (C) Fergus Duncan 2015
#

import sys
import time
import serial
import threading

VP2P_UV       = 0x4 # UV index
VP2P_RAINSECS = 0x5 # seconds between rain bucket tips
VP2P_SOLAR    = 0x6 # solar irradiation
VP2P_TEMP     = 0x8 # outside temperature
VP2P_WINDGUST = 0x9 # 10-minute wind gust
VP2P_HUMIDITY = 0xA # outside humidity
VP2P_RAIN     = 0xE # rain bucket tips counter

def processIstring(string) :
    print "ISS packet : ", string
    fields = string.strip().split()
    try :
        byte0 = int(fields[2],16)
        byte1 = int(fields[3],16)
        byte2 = int(fields[4],16)
        byte3 = int(fields[5],16)
        byte4 = int(fields[6],16)
        byte5 = int(fields[7],16)
        byte6 = int(fields[8],16)
        byte7 = int(fields[9],16)
    except :
        print "Invalid Packet"
        return;

    # checksum is verified by the monteino firmware
    # checking it here is a little OTT

    transmitterId = byte0 & 0x07
    print "Transmitter ID : ", transmitterId

    batteryStatus = (byte0 & 0x08) >> 3;
    print "Battery Status : ", batteryStatus

    windSpeed = byte1;
    windDirection = (byte2 * 360) / 255;
    print "Wind : ", windSpeed, "@", windDirection

    packetType = byte0 >> 4

    if packetType == VP2P_UV :
        print "VP2P_UV"
    elif packetType == VP2P_RAINSECS :
        print"VP2P_RAINSECS"
        if byte3 == 0xff :
            # no rain
            print "No Rain"
            rainRate = 0
        elif (byte4 & 0x40) == 0 :
            # light rain
            # 720 / (((Byte4 && 0x30) / 16 * 250) + Byte3)
            rainRate = 720 / (((byte4 & 0x30) / 16 * 250) + byte3)
        elif (byte4 & 0x40) == 0x40 :
            # strong rain
            # 11520 / (((Byte4 && 0x30) / 16 * 250) + Byte3)
            rainRate = 11520 / (((byte4 & 0x30) / 16 * 250) + byte3)
        print "Rain Rate : ",rainRate
    elif packetType == VP2P_SOLAR :
        print"VP2P_SOLAR"
    elif packetType == VP2P_TEMP :
        print"VP2P_TEMP"
        externalTemperature10xF = (((byte3 << 8) + (byte4)) >> 4);
        externalTemperatureF = float(externalTemperature10xF) / 10
        externalTemperature10xC = (((externalTemperature10xF-320)*5)/9);
        externalTemperatureC = float(externalTemperature10xC) / 10
        print "Temp : ",externalTemperatureC,"C(",externalTemperatureF,"F)"
    elif packetType == VP2P_WINDGUST :
        print"VP2P_WINDGUST"
        windGust = byte3;
        print "Wind Gust : ", windGust
    elif packetType == VP2P_HUMIDITY :
        print"VP2P_HUMIDITY"
        externalHumidity = (((byte4 & 0xf0) << 4) + byte3) / 10
        print "Humidity : ",externalHumidity,"%"
    elif packetType == VP2P_RAIN :
        print"VP2P_RAIN"
	rainTicks = byte3;
        print "Rain Ticks : ", rainTicks
    else :
        print "Unknown Packet Type"

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
    ser.flushInput()

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
#		    print string
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
