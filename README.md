# NMEA utilities

![ci](https://github.com/geospace-code/nmeautils/workflows/ci/badge.svg)

Python-based NMEA (ascii) reader, and a SCPI reader for Jackson Labs GPS

* nmealog.py: multithreaded NMEA serial port reader with selectable polling cadence.
* SCPIlogger.py: for Jackson Labs GPS receivers that use SCPI. It's not a raw NMEA output, but query   based.                          |

## Installation

```sh
pip install -e .
```

## Examples

For a Garmin GPS or other GPS with NMEA output:

```sh
python nmealog.py -l out.txt -p /dev/ttyUSB0 -T 1
```

For a Jackson Labs SCPI-based GPS:

```sh
python SCPIlogger.py -l out.txt -p /dev/ttyUSB0 -T 1
```

### Jackson Labs GPS SCPI commands

Here are but a few of the powerful SCPI commands you can send to a
Jackson Labs GPS receiver. Note the default baudrate is 115200, NO
hardware / software flow control, 8-N-1.

 SCPI | result
------|--------
`\*IDN?` | identify receiver (model #, firmware revision
`GPS:SAT:VIS:COUN?` | How many GPS satellites are visible per the almanac, above the 0 degree horizon
`GPS:SAT:TRA:COUN?` | How many GPS satellites are actually being received
`SYNC:HOLD:DUR?` | Holdover duration
`GPS:JAM?` | Estimated jamming level
`PTIME:TINT?` | Time offset

## Reference

Another project to consider: [pynmea2](https://github.com/Knio/pynmea2)
