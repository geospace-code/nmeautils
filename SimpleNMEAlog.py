#!/usr/bin/env python
import logging
from pprint import pprint

from nmeautils.nmea import nmeapoll

if __name__ == "__main__":
    from argparse import ArgumentParser

    p = ArgumentParser()
    p.add_argument("port", help="port GPS is on e.g.  COM1   /dev/ttyUSB0")
    p.add_argument("baud", help="baud rate e.g. 4800", type=int)
    p.add_argument("sentence", help=" sentence to parse. E.g. GPRMC")
    p = p.parse_args()

    dat = nmeapoll(p.port, p.baud, p.sentence)
    if dat is not None:
        pprint(dat)
    else:
        logging.error("no GPS fix")
