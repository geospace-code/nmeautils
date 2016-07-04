#!/usr/bin/env python
from re import sub

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
    try:
        if hex(csum) == hex(int(cksum, 16)):
            return True
    except ValueError: #some truncated lines really mess up
        pass

    return False
