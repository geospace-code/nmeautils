#!/usr/bin/env python
from __future__ import print_function
from sys import stderr

from nmeautils import nmeapoll

if __name__ == '__main__':

    dat = nmeapoll()
    if dat is not None:
        print(dat)
    else:
        print('no GPS fix',file=stderr)