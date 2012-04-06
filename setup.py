#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

try:
    import py2exe
except ImportError:
    pass

setup(name="restoretools",
      version='0.1',
      author='Lev Shamardin',
      author_email='shamardin@gmail.com',
      license='MIT',
      scripts=['calllog2xml.py', 'mmssms2xml.py', 'extract.py'],
      platforms=['linux', 'win32'],
      windows=['extract.py'],
      )
