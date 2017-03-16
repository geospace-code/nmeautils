#!/usr/bin/env python
from setuptools import setup

req = ['pyserial']

setup(name='nmeautils',
      packages=['nmeautils'],
	  description='read NMEA with Python',
	  author='Michael Hirsch, Ph.D.',
	  url='https://github.com/scivision/nmeautils',
      install_requires=req,
	  )

