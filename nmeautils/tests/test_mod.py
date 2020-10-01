from datetime import datetime
from pytest import approx

from nmeautils.nmea import chksum_nmea, nmeapoll
from nmeautils import Simport

gprmc1 = "$GPRMC,225446,A,4916.45,N,12311.12,W,000.5,054.7,191104,020.3,E*61"


def test_checksum():
    assert not chksum_nmea("wefo32f32")

    assert chksum_nmea(gprmc1)


def test_simpleparser():
    dat = nmeapoll(Simport(gprmc1), 4800, "GPRMC")
    assert dat["t"] == datetime(2004, 11, 19, 22, 54, 46)
    assert dat["lat"] == approx(49.2666666666)
    assert dat["lon"] == approx(-123.1833333333)
