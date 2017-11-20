#!/usr/bin/env python
req = ['pyserial','nose','numpy']
# %%
from setuptools import setup, find_packages

setup(name='nmeautils',
      packages=find_packages(),
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
      install_requires=req,
      python_requires='>=3.6',
	  )

