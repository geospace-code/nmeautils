[![Code Climate](https://codeclimate.com/github/scienceopen/nmeautils/badges/gpa.svg)](https://codeclimate.com/github/scienceopen/nmeautils)
[![Health](https://landscape.io/github/scienceopen/nmea-util/master/landscape.png)](https://landscape.io/github/scienceopen/nmea-util/master)

nmea-util
=========

Python-based NMEA (ascii) reader, and a SCPI reader for Jackson Labs GPS

``` nmealog.py ``` is a non-blocking multithreaded NMEA serial port reader 
that I use with my Garmin GPS. It allows you to select polling cadence.

``` SCPIlogger.py `` is for the Jackson Labs GPS receivers that use SCPI, it's not a raw NMEA output, but rather it's query based.

Installation
------------
```
git clone https://github.com/scienceopen/nmea-util
conda install --file requirements.txt
```

Example usage
-------------
```
python nmealog.py -l out.txt -p /dev/ttyUSB0 -T 1
```

```
pyton SCPIlogger.py -l out.txt -p /dev/ttyUSB0 -T 1
```



Also checkout

https://github.com/Knio/pynmea2
