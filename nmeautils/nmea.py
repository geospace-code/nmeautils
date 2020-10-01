from datetime import datetime, time
import serial
from time import sleep
import typing

from . import Simport


def nmeapoll(port: str, baud: int, sentence: str) -> typing.Dict[str, typing.Any]:
    """
    grab vital GPS data, return dict of parsed data

    inspired by work from Zachary Chapasko
    Michael Hirsch

    example for GPS receiver at 4800 baud on COM1, selecting GPGGA

    nmea = nmeapoll('COM1',4800,'GPGGA')
    """

    sentence = sentence.upper()

    if isinstance(port, str) and port != "sim":  # normal
        with serial.Serial(port, baud, 8, "N", 1) as S:
            gstr = nmeagrab(S, port, sentence)
    else:  # self test
        if port == "sim":
            S = Simport("$GPRMC,225446,A,4916.45,N,12311.12,W,000.5,054.7,191104,020.3,E*61")
        else:  # simport input
            S = port
        gstr = nmeagrab(S, None, sentence)

    nmea = nmeaparser(gstr, sentence)

    return nmea


def nmeagrab(S, port: str, sentence: str) -> str:
    assert S.isOpen(), "failed to open {}".format(port)

    # prepare two strings for message parsing
    gpsb = b""
    pat = b"$" + bytes(sentence, "ascii")
    gpsstr = ""

    while not gpsb:
        bwait = S.inWaiting()
        if bwait > 81:  # max NMEA length is 80 bytes (variable) (and need line ending 80+1)
            gpsb = S.readline()
            if not (gpsb.startswith(pat) and chksum_nmea(gpsb)):
                gpsstr = ""
                print("waiting for GPS, buffer bytes", bwait)
                sleep(0.1)
            else:
                gpsstr = gpsb.decode("ascii")

    return gpsstr


def nmeaparser(gstr: str, sentence: str) -> typing.Dict[str, typing.Any]:

    if sentence == "GPGGA":
        nmea = parsegpgga(gstr)
    elif sentence == "GPRMC":
        nmea = parsegprmc(gstr)
    else:
        raise NotImplementedError("unknown NMEA type {}".format(sentence))

    return nmea


def parsegprmc(gstr: str) -> typing.Dict[str, typing.Any]:
    lg = gstr.split(",")

    if lg[2] == "V":  # we don't have a GPS fix
        return None

    nmea = {
        "t": nmeadatetime(lg[9], lg[1]),
        "lat": splitdec(lg[3:5], "S"),
        "lon": splitdec(lg[5:7], "W"),
    }

    return nmea


def parsegpgga(gstr: str) -> typing.Dict[str, typing.Any]:
    lg = gstr.split(",")

    if lg[6] == "0":  # we don't have a GPS fix
        return None
    # %%  prepare final result
    nmea = {
        "t": nmeatime(lg[1]),  # UTC HHMMSS
        "lat": splitdec(lg[2:4], "S"),
        "lon": splitdec(lg[4:6], "W"),
        "alt": float(lg[9]),  # meters
    }

    return nmea


def nmeadatetime(D: str, T: str) -> datetime:
    return datetime(
        2000 + int(D[4:6]), int(D[2:4]), int(D[:2]), int(T[:-4]), int(T[-4:-2]), int(T[-2:])
    )


def nmeatime(G: str) -> time:
    return time(int(G[:-4]), int(G[-4:-2]), int(G[-2:]))


def splitdec(G: typing.Sequence[str], neg: str) -> float:
    """
    accounts for variable width by hinging at decimal point
    """
    dec = G[0].split(".")
    dd = float(dec[0][:-2]) + float(dec[0][-2:]) / 60.0

    if G[1] == neg:
        dd = -dd

    return dd


def chksum_nmea(sentence: typing.Union[bytes, str]) -> bool:
    """
    http://doschman.blogspot.com/2013/01/calculating-nmea-sentence-checksums.html

    Michael Hirsch, Ph.D.
    """
    if isinstance(sentence, bytes):
        try:
            sentence = sentence.decode("ascii")
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
    except ValueError:  # some truncated lines really mess up
        return False
