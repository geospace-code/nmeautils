#!/usr/bin/env python
req = ['pyserial','nose','numpy']
# %%
import pip
try:
    import conda.cli
    conda.cli.main('install',*req)
except Exception as e:
    pip.main(['install'] +req)
# %%
from setuptools import setup

setup(name='nmeautils',
      packages=['nmeautils'],
      version='1.0',
	  description='read/parse NMEA with Python',
	  author='Michael Hirsch, Ph.D.',
	  url='https://github.com/scivision/nmeautils',
      classifiers=[
          'Intended Audience :: Science/Research',
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Topic :: Scientific/Engineering',
          'Programming Language :: Python :: 3',
          ],
	  )

