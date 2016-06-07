#!/usr/bin/env python
from setuptools import setup
import subprocess

try:
    subprocess.call(['conda','install','--yes','--file','requirements.txt'])
except (Exception,KeyboardInterrupt) as e:
    pass

with open('README.rst','r') as f:
	long_description = f.read()

setup(name='nmeautils',
	  description='read NMEA with Python',
	  long_description=long_description,
	  author='Michael Hirsch',
	  url='https://github.com/scienceopen/nmeautils',
      install_requires=[ 'pathlib2'],
	  )

