#!/usr/bin/env python
'''
Jackson Labs Firefly-II and ULN-2550 GPS logger
that allows logging every N seconds,
even when GPS is giving data every second.
This is NOT an NMEA logger, it uses SCPI over serial port
Michael Hirsch
https://scivision.co

Note: Jackson Labs default baud rate is 115200
'''
from sys import exit
from serial import Serial
from pathlib import Path
from time import sleep
from signal import signal,SIGINT
from datetime import datetime, date

def nmeapoll(sport,logstem,period,verbose):

    if sport == '/dev/null': #simulation mode
        from nmeautils import Simport
        print('simulation open')
        S = Simport()
    else:
        # create a Serial object to manipulate the serial port
        S = Serial(sport,baudrate=19200,timeout=1,bytesize=8,
                   parity='N',stopbits=1,xonxoff=0,rtscts=0)

    if S.isOpen():
       S.close()

    S.open()

    #let's clear out any old junk
    S.flushInput()
    S.flushOutput()

    S.write("*IDN?\r\n")
    txt = S.readlines()[1].decode('utf-8')
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
        S.write("GPS:JAM?\r\n")
        jam = S.readlines()[1].decode('utf-8') #[1].rstrip('\r\n')
        # get number of visible sats per almanac
        S.write("GPS:SAT:VIS:COUN?\r\n")
        nVis = S.readlines()[1].decode('utf-8')
        # get number of actually tracked satellites
        S.write("GPS:SAT:TRA:COUN?\r\n")
        nTrk = S.readlines()[1].decode('utf-8')
        #time offset
        S.write("PTIME:TINT?\r\n")
        tint = S.readlines()[1].decode('utf-8')
        #holdover duration
        S.write("SYNC:HOLD:DUR?\r\n")
        hdur = S.readlines()[1].decode('utf-8')

    	  #write results to disk
        cln=[now,jam,nVis,nTrk,tint,hdur]
        cln=' '.join(cln)+ '\n'
        if verbose:
            print(cln)

        if logstem is not None:
            logfn = Path(logstem).expanduser() +'-' + LastDay.strftime('%Y-%m-%d') + '.txt'
            with logfn.open("a") as f:
                f.write(cln)

        sleep(period)

def parsestat(statint):
    """ from page 18 sec. 3.3.5.1 of Fury 1.22 manual """
    # same as matlab/octave de2bi(statint,16,2,'left-msb')
    statbin = '{:016b}'.format(statint)
    print(statbin)

def signal_handler(signal, frame):
    print('\n Aborting program as per user request! \n')
    exit()


if __name__ == '__main__':
    from argparse import ArgumentParser
    signal(SIGINT, signal_handler) #allow Ctrl C to nicely abort program

    p = ArgumentParser(description='Interacts with Jackson Labs GPS NMEA')
    p.add_argument('-o','--log',help='specify log file to write GPS data to')
    p.add_argument('-p','--port',help='specify serial port to listen on',default='/dev/ttyS0')
    p.add_argument('-v','--verbose',help='print a lot of stuff to help debug',action='store_true')
    p.add_argument('-T','--period',help='polling period (default 10 seconds)',type=float,default=10.)
    args = p.parse_args()

    nmeapoll(args.port, args.log, args.period, args.verbose)

