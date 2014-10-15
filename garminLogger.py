#!/usr/bin/env python3
'''
 Crude NMEA logger that allows logging every N seconds,
 even when GPS is giving data every second.
 Probably a bad example of using the serial port! consider Python asyncio
 Michael Hirsch
 GPL v3+ license

tested in Python 2.7 and 3.4 with PySerial 2.7

REQUIRES PySerial, obtained via
 (linux)
 pip install pyserial
 or (windows with Anaconda)
 conda install pyserial
'''
from serial import Serial
from time import sleep
from os.path import expanduser,splitext
from signal import signal, SIGINT
from datetime import date
from re import sub

def nmeapoll(sport,logfn,period,verbose):

    nline = 4
    bytesWait = 500 #wait to read till this many bytes are in buffer

    # create a Serial object to manipulate the serial port
    hs = Serial(sport, baudrate=19200, timeout=1, bytesize=8,
                       parity='N', stopbits=1, xonxoff=0, rtscts=0)

    #is the serial port open? if not, open it
    if not hs.isOpen():
        print('opening port ' + sport)
        hs.open()

    #let's clear out any old junk
    hs.flushInput()
    hs.flushOutput()

    lastday = date.today()

    # this loops waits for enough bytes in the buffer before proceeding
    # this is a very old fashioned way to do this, and is not perfect!
    while True:
        # now let next NMEA batch arrive
        inBufferByte = hs.inWaiting()
        if inBufferByte < bytesWait:
            if verbose:
               print(inBufferByte)
            sleep(0.5) #wait some more for buffer to fill (0.5 seconds)

            #check date
        else: # we have enough bytes to read the buffer
            lastday = readbuf(hs,lastday,logfn,nline,verbose)
            sleep(period-2.5) #empirical
            hs.flushInput()

def readbuf(hs,LastDay,logfn,nline,verbose):
    Today = date.today()
    if (Today-LastDay).days > 0:
        LastDay = Today #rollover to the next day

    if logfn is not None:
        logfn = expanduser(splitext(logfn)[0]) + '-' + LastDay.strftime('%Y-%m-%d') + '.txt'

    txt = []
    # get latest NMEA ASCII from Garmin
    for i in range(nline):
        line = hs.readline().decode('utf-8')
        if chksum_nmea(line):
            txt.append(line)

    #write results to disk
    cgrp=''.join(txt)
    if verbose:
        print(cgrp)

    if logfn is not None:
        with open(logfn,"a") as fid:
            fid.write(cgrp)
    elif not verbose:
        print(cgrp) #will print to screen if not already verbose

    return LastDay

def chksum_nmea(sentence):
    '''
    from http://doschman.blogspot.com/2013/01/calculating-nmea-sentence-checksums.html
    '''
    # This is a string, will need to convert it to hex for
    # proper comparsion below
    cksum = sentence[-4:-2]

    # String slicing: Grabs all the characters
    # between '$' and '*' and nukes any lingering
    # newline or CRLF
    chksumdata = sub("(\n|\r\n)","", sentence[sentence.find("$")+1:sentence.find("*")])

    # Initializing our first XOR value
    csum = 0

    # For each char in chksumdata, XOR against the previous
    # XOR'd char.  The final XOR of the last char will be our
    # checksum to verify against the checksum we sliced off
    # the NMEA sentence

    for c in chksumdata:
        # XOR'ing value of csum against the next char in line
        # and storing the new XOR value in csum
        csum ^= ord(c)

    # Do we have a validated sentence?
    if hex(csum) == hex(int(cksum, 16)):
        return True

    return False


def signal_handler(signal, frame):
    print('\n *** Aborting program as per user pressed Ctrl+C ! \n')
    exit(0)

if __name__ == '__main__':
    from argparse import ArgumentParser
    signal(SIGINT, signal_handler) #allow Ctrl C to nicely abort program

    p = ArgumentParser(description='listens to Garmin NMEA')
    p.add_argument('-l','--log',help='specify log file to write GPS data to',type=str,default=None)
    p.add_argument('-p','--port',help='specify serial port to listen on',type=str,default='/dev/ttyS0')
    p.add_argument('-v','--verbose',help='print a lot of stuff to help debug',action='store_true')
    p.add_argument('-T','--period',help='polling period (default 10 seconds)',type=float,default=10)
    args = p.parse_args()

    nmeapoll(args.port, args.log, args.period, args.verbose)
