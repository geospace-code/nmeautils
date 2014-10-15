#!/usr/bin/env python3
'''
 Jackson Labs Firefly-II and ULN-2550 GPS logger
 that allows logging every N seconds,
 even when GPS is giving data every second.
 This is NOT an NMEA logger, it uses SCPI over serial port
 Michael Hirsch
 http://blogs.bu.edu/mhirsch
 GPL v3+ license

 tested in Python 2.7 and 3.4 with PySerial 2.7

REQUIRES PySerial, obtained via
 (linux)
 pip install pyserial
 or (windows with Anaconda)
 conda install pyserial
'''
from serial import Serial
from os.path import expanduser,splitext
from time import sleep
from signal import signal,SIGINT
from datetime import datetime, date

def nmeapoll(sport,logfn,period,verbose):

    # create a Serial object to manipulate the serial port
    hs = Serial(sport,baud=19200,timeout=1,bytesize=8,
                       parity='N',stopbits=1,xonxoff=0,rtscts=0)

    if not hs.isOpen():
       print('opening port ' + hs.name)
       hs.open()

    #let's clear out any old junk
    hs.flushInput()
    hs.flushOutput()

    hs.write("*IDN?\r\n")
    txt=hs.readlines()[1].decode('utf-8')
    print(txt)

    LastDay = date.today()
    print('starting read loop')

    while True:
        #check date
        Today = date.today()
        if (Today-LastDay).days > 0:
            LastDay = Today


        #get beginning of read time
        now=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        # get jamming level
        hs.write("GPS:JAM?\r\n")
        jam=hs.readlines()[1].decode('utf-8') #[1].rstrip('\r\n')
        # get number of visible sats per almanac
        hs.write("GPS:SAT:VIS:COUN?\r\n")
        nVis=hs.readlines()[1].decode('utf-8')
        # get number of actually tracked satellites
        hs.write("GPS:SAT:TRA:COUN?\r\n")
        nTrk=hs.readlines()[1].decode('utf-8')
        #time offset
        hs.write("PTIME:TINT?\r\n")
        tint=hs.readlines()[1].decode('utf-8')
        #holdover duration
        hs.write("SYNC:HOLD:DUR?\r\n")
        hdur=hs.readlines()[1].decode('utf-8')

    	  #write results to disk
        cln=[now,jam,nVis,nTrk,tint,hdur]
        cln=' '.join(cln)+ '\n'
        if verbose:
            print(cln)

        if logfn is not None:
            logfn = expanduser(splitext(logfn)[0]) + '-' + LastDay.strftime('%Y-%m-%d') + '.txt'
            with open(logfn,"a") as fid:
                fid.write(cln)

        sleep(period)

def signal_handler(signal, frame):
    print('\n *** Aborting program as per user pressed Ctrl+C ! \n')
    exit(0)

if __name__ == '__main__':
    from argparse import ArgumentParser
    signal(SIGINT, signal_handler) #allow Ctrl C to nicely abort program

    p = ArgumentParser(description='Interacts with Jackson Labs GPS NMEA')
    p.add_argument('-l','--log',help='specify log file to write GPS data to',type=str,default=None)
    p.add_argument('-p','--port',help='specify serial port to listen on',type=str,default='/dev/ttyS0')
    p.add_argument('-v','--verbose',help='print a lot of stuff to help debug',action='store_true')
    p.add_argument('-T','--period',help='polling period (default 10 seconds)',type=float,default=10)
    args = p.parse_args()

    nmeapoll(args.port, args.log, args.period, args.verbose)

