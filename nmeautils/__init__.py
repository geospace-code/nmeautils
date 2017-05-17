from os import devnull
from datetime import datetime,time
import serial
from time import sleep

def nmeapoll(port,baud,sentence):
    """
    grab vital GPS data, return dict of parsed data
    
    nspired by work from Zachary Chapasko
    Michael hirsch, Ph.D.
    
    example for GPS receiver at 4800 baud on COM1, selecting GPGGA
    
    nmea = nmeapoll('COM1',4800,'GPGGA')    
    """
    assert isinstance(sentence,(str,bytes))
    
    sentence = sentence.upper()
    
    if isinstance(port,str) and port != 'sim':  # normal
        with serial.Serial(port, baud, 8, 'N', 1) as S:
            gstr = nmeagrab(S,port,sentence)
    else: # self test
        if port == 'sim':
            port = Simport( '$GPRMC,225446,A,4916.45,N,12311.12,W,000.5,054.7,191104,020.3,E*61')
        gstr = nmeagrab(port,None,sentence)

    nmea = nmeaparser(gstr,sentence)

    return nmea

def nmeagrab(S,port,sentence):
    assert S.isOpen(),'failed to open {}'.format(port)

    # prepare two strings for message parsing
    gpsstr = ''
    pat = b'$'+ bytes(sentence, 'ascii')
    
    while not gpsstr:
        bwait = S.inWaiting()
        if bwait > 81:          # max NMEA length is 80 bytes (variable) (and need line ending 80+1)
            gpsstr = S.readline()
            if not (gpsstr.startswith(pat) and chksum_nmea(gpsstr)):
                gpsstr = ''
                print('waiting for GPS, buffer bytes',bwait)
                sleep(0.1)
            else:
                gpsstr = gpsstr.decode('ascii')
                
    return gpsstr

def nmeaparser(gstr,sentence):

    if sentence == 'GPGGA':
        nmea = parsegpgga(gstr)
    elif sentence == 'GPRMC':
        nmea= parsegprmc(gstr)
    else:
        raise NotImplementedError('unknown NMEA type {}'.format(sentence))
        
    return nmea
        
def parsegprmc(gstr):
    lg = gstr.split(',')
    
    if lg[2] == 'V': # we don't have a GPS fix
        return
    
    nmea = {
            't': nmeadatetime(lg[9],lg[1]),
            'lat': splitdec(lg[3:5], 'S'),
            'lon': splitdec(lg[5:7], 'W'),
            }
    
    return nmea
    

def parsegpgga(gstr):
    lg = gstr.split(',')

    if lg[6] == '0':  # we don't have a GPS fix
        return
# %%  prepare final result
    nmea = {
           't': nmeatime(lg[1]),  # UTC HHMMSS
           'lat': splitdec(lg[2:4], 'S'),
           'lon': splitdec(lg[4:6], 'W'),
           'alt': float(lg[9])  # meters
            }
    
    return nmea

def nmeadatetime(D,T):
    return datetime(2000+int(D[4:6]), int(D[2:4]), int(D[:2]),
                    int(T[:-4]), int(T[-4:-2]), int(T[-2:]))
    
def nmeatime(G):
    return time(G[:-4], G[-4:-2], G[-2:])

def splitdec(G,neg):
    """
    accounts for variable width by hinging at decimal point
    """
    dec = G[0].split('.');
    dd = float(dec[0][:-2]) + float(dec[0][-2:])/60.

    if G[1] == neg:
        dd = -dd

    return dd



def chksum_nmea(sentence):
    '''
    http://doschman.blogspot.com/2013/01/calculating-nmea-sentence-checksums.html

    Michael Hirsch, Ph.D.
    '''
    if isinstance(sentence,bytes):
        try:
            sentence = sentence.decode('ascii')
        except TypeError:
            return False
        
    sentence = sentence.strip()
    
    cksum = sentence.strip()[-2:]

    chksumdata = sentence[1:-3]  # discards $ and *
   
    # Initializing our first XOR value
    csum = 0
    """
    For each char in chksumdata, XOR against the previous XOR'd char.
    The final XOR of the last char will be our checksum to verify against the checksum we sliced off
    the NMEA sentence
    """

    for c in chksumdata:
        # XOR'ing value of csum against the next char in line
        # and storing the new XOR value in csum
        csum ^= ord(c)

# %% Do we have a validated sentence?
    try:
        return hex(csum) == hex(int(cksum, 16))
    except ValueError: #some truncated lines really mess up
        return False

class Simport():
    """
    for selftest only
    """
    def __init__(self,sentence=None):
        self.f = devnull
        self.sentence = sentence

    def isOpen(self):
        return True

    def write(self, cmd):
        with open(self.f, 'w') as f:
            f.write(cmd)

    def open(self):
        pass

    def close(self):
        pass

    def flushInput(self):
        pass
    def flushOutput(self):
        pass

    def readline(self):
        if self.sentence:
            return bytes(self.sentence, 'ascii')
        else:
            return b'simulation'

    def readlines(self):
        if self.sentence:
            return [bytes(self.sentence, 'ascii')]
        else:
            return [b'simulation']

    def inWaiting(self):
        return 1024
