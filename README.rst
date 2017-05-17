.. image:: https://travis-ci.org/scivision/nmeautils.svg?branch=master
    :target: https://travis-ci.org/scivision/nmeautils

=========   
nmeautils
=========

Python-based NMEA (ascii) reader, and a SCPI reader for Jackson Labs GPS

============== =========
nmealog.py     non-blocking multithreaded NMEA serial port reader (e.g. Garmin), selectable polling cadence.
SCPIlogger.py   Jackson Labs GPS receivers that use SCPI, it's not a raw NMEA output, but rather it's query based.
============== =========

Installation
------------
::

    python setup.py develop

Examples
--------
For a Garmin GPS or other GPS with NMEA output::

    python nmealog.py -l out.txt -p /dev/ttyUSB0 -T 1

For a Jackson Labs SCPI-based GPS::

    python SCPIlogger.py -l out.txt -p /dev/ttyUSB0 -T 1


Jackson Labs GPS SCPI commands
------------------------------
Here are but a few of the powerful SCPI commands you can send to a Jackson Labs GPS receiver.
Note the default baudrate is 115200, NO hardware/software flow control, 8-N-1.

=================  ========
SCPI commands	   result
=================  ========
\*IDN?              identify receiver (model #, firmware revision)
GPS:SAT:VIS:COUN?   How many GPS satellites are visible (per the almanac, above the 0 degree horizon)
GPS:SAT:TRA:COUN?   How many GPS satellites are actually being received
SYNC:HOLD:DUR?      Holdover duration
GPS:JAM?            Estimated jamming level
PTIME:TINT?         Time offset
=================  ========

Reference
---------

Another project to consider:  https://github.com/Knio/pynmea2
