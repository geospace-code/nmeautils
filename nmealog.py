#!/usr/bin/env python
'''
 Multithreaded NMEA serial port logger that allows logging every N seconds,
 even when GPS is giving data every second.
 Michael Hirsch

An example of using non-blocking threading for serial port reading.
Note: python will be switching back and forth, processing one thread at a time.
This is just fine for thread(s) that sleep most of the time like here.
For parallel processing that bypasses the GIL, consider the multiprocessing module

tested in Python 2.7 and 3 with PySerial 2.7

This could also be done with asyncio
'''
from threading import Thread,Event
from serial import Serial
from time import sleep
from signal import signal, SIGINT
from datetime import date
from datetime import datetime as dt
#
from nmeautils import chksum_nmea

def nmeapoll(sport,logfn,period,baud,verbose):

    nline = 4
    bytesWait = 500 #wait to read till this many bytes are in buffer

    if sport == '/dev/null': #simulation mode
        from nmeautils import Simport
        print('simulation open')
        S = Simport()
    else:
    # create a Serial object to manipulate the serial port
        S = Serial(sport, baudrate=baud, timeout=1, bytesize=8,
                       parity='N', stopbits=1, xonxoff=0, rtscts=0)

    if S.isOpen():
        S.close()

    S.open()

    #let's clear out any old junk
    S.flushInput()
    S.flushOutput()

    lastday = date.today()

    #start non-blocking read
    stop = Event()
    thread = Thread(target=portthread,
                    args=(S,lastday,logfn,nline,verbose,bytesWait,period,stop))
    thread.start()

    # we put this after the thread so it knows how to stop the thread
    def signal_handler(*args):
        stop.set()
        print('\n *** Aborting program as per user pressed Ctrl+C ! \n')
        raise SystemExit()
    signal(SIGINT,signal_handler)
    #silly printing to show we're not blocking
    while True:
        print('current time is ' + dt.utcnow().strftime('%H:%M:%S'))
        sleep(1)

def portthread(S,lastday,logfn,nline,verbose,bytesWait,period,stop):
    # this loops waits for enough bytes in the buffer before proceeding
    while(not stop.is_set()):
        # now let next NMEA batch arrive
        inBufferByte = S.inWaiting()
        if inBufferByte < bytesWait:
            if verbose:
               print(inBufferByte)
            stop.wait(0.5) #wait some more for buffer to fill (0.5 seconds)

            #check date
        else: # we have enough bytes to read the buffer
            readbuf(S,lastday,logfn,nline,verbose)
            stop.wait(period-2.5) #empirical
            S.flushInput()

def readbuf(S,lastday,logstem,nline,verbose):
    Today = date.today()
    if (Today-lastday).days > 0:
        lastday = Today #rollover to the next day

    txt = []
    # get latest NMEA ASCII from Garmin
    for i in range(nline):
        line = S.readline().decode('utf-8')
        if chksum_nmea(line):
            txt.append(line)

    #write results to disk
    cgrp=''.join(txt)
    if verbose:
        print(cgrp)

    if logstem is not None:
        logfn = f'{logstem}-{lastday.strftime("%Y-%m-%d")}.log'
        with open(logfn,"a") as f:
            f.write(cgrp)
    elif not verbose:
        print(cgrp) #will print to screen if not already verbose


if __name__ == '__main__':
    from argparse import ArgumentParser

    p = ArgumentParser(description='listens to Garmin NMEA')
    p.add_argument('-o','--log',help='specify log file to write GPS data to')
    p.add_argument('-p','--port',help='specify serial port to listen on',default='/dev/ttyS0')
    p.add_argument('-v','--verbose',help='print a lot of stuff to help debug',action='store_true')
    p.add_argument('-T','--period',help='polling period (default 10 seconds)',type=float,default=10)
    p.add_argument('-b','--baud',help='baud rate (default 19200)',type=int,default=19200)
    p = p.parse_args()

    nmeapoll(p.port, p.log, p.period, p.baud, p.verbose)
