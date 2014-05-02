# Jackson Labs Firefly-II and ULN-2550 GPS logger 
# that allows logging every N seconds, 
# even when GPS is giving data every second.
# This is NOT an NMEA logger, it uses SCPI over serial port
# Michael Hirsch
# http://blogs.bu.edu/mhirsch
# GPL v3+ license

import serial, time, io
import signal,sys
from datetime import datetime, date, timedelta

def sigexit(signal, frame):
        print('Exiting')
        hs.close()
        sys.exit(0)
signal.signal(signal.SIGINT,sigexit)

if len(sys.argv)>1: sport=sys.argv[1]
else: sport = '/dev/ttyS7'

baud=19200

verbose = False

logStem="../GPSlog/JacksonGPS"
logExt=".txt"

hs = serial.Serial(sport,baud,timeout=1,bytesize=8,
                   parity='N',stopbits=1,xonxoff=0,rtscts=0)

if not hs.isOpen():
   print(hs.name)
   hs.open()

hs.flushInput()
hs.flushOutput()

hs.write("*IDN?\r\n") 
idTxt=hs.readlines()[1].rstrip('\r\n')
print(idTxt)

LastDay = date.today()
print('starting read loop')

while True:
   #check date 
   Today = date.today()
   if (Today-LastDay).days > 0:
      LastDay = Today
   logFN = logStem + '-' + LastDay.strftime('%Y-%m-%d') + logExt
   #get beginning of read time
   now=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
   # get jamming level
   hs.write("GPS:JAM?\r\n")
   jam=hs.readlines()[1].rstrip('\r\n')
   # get number of visible sats per almanac
   hs.write("GPS:SAT:VIS:COUN?\r\n")
	nVis=hs.readlines()[1].rstrip('\r\n')
	# get number of actually tracked satellites
	hs.write("GPS:SAT:TRA:COUN?\r\n")
	nTrk=hs.readlines()[1].rstrip('\r\n')
   #time offset
   hs.write("PTIME:TINT?\r\n")
   tint=hs.readlines()[1].rstrip('\r\n')
 	#holdover duration
	hs.write("SYNC:HOLD:DUR?\r\n")	
	hdur=hs.readlines()[1].rstrip('\r\n')

	#write results to disk
   cln=[now,jam,nVis,nTrk,tint,hdur]
   cln=' '.join(cln)
	if verbose:
	   print(cln)
	cln+='\r\n' #for proper file writing

	with open(logFN,"a") as fl:
	   fl.write(cln)
	time.sleep(5)
