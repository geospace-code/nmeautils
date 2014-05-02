# Crude NMEA logger that allows logging every N seconds, 
# even when GPS is giving data every second.
# Michael Hirsch
# http://blogs.bu.edu/mhirsch
# GPL v3+ license

import serial, time
import os
import signal, sys
from datetime import datetime, date, timedelta

def sigexit(in1, in2):
    print('  Exiting Garmin Logger by user SIGINT')
    hs.close() 
    sys.exit(0)
signal.signal(signal.SIGINT, sigexit)

logStem = os.path.expanduser('~/GPSlog/GarminLog')
logExt = '.txt'
if len(sys.argv)>1: sport=sys.argv[1]
else: sport = '/dev/ttyS0'
nline = 6
period = 10
verbose = True
bytesWait = 500

hs = serial.Serial(sport, 19200, timeout=1, bytesize=8,
                   parity='N', stopbits=1, xonxoff=0, rtscts=0)

if not hs.isOpen():
    print('opening port')
    hs.open()

hs.flushInput()
hs.flushOutput()

idTxt = [None]*(nline+1)
LastDay = date.today()
print('starting read loop')
while True:
    # now let next NMEA batch arrive
    inBufferByte = hs.inWaiting()
    if inBufferByte < bytesWait:
        if verbose:
           print(inBufferByte)
        time.sleep(0.5)
	continue
    #check date 
    Today = date.today()
    if (Today-LastDay).days > 0:
    LastDay = Today
    
    logFN = logStem + '-' + LastDay.strftime('%Y-%m-%d') + logExt
    
    # get latest text from Garmin
    for li in range(nline+1):
        idTxt[li] = hs.readline()
    #write results to disk
    cgrp=''.join(idTxt)
    if verbose:
        print(cgrp)

    cgrp = cgrp + '\r\n'
    with open(logFN,"a") as fl:
        fl.write(cgrp)
        
    time.sleep(period-2)
    hs.flushInput()




