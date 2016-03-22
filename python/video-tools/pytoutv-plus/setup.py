#!/usr/bin/env python

import sys
from setuptools import setup


# Make sure we run Python 3 here
v = sys.version_info
if v.major < 3:
    sys.exit('Sorry, pytoutv_plus needs Python 3')

entry_points = {
    'console_scripts': [
        'toutv = pytoutv_plus.app:run'
    ],
}
setup_requires = [
    'pytoutv>=2.3.0',
    'setuptools',
]

setup(name='pytoutv_plus',
      version='0.1',
      entry_points=entry_points,
      packages=['pytoutv_plus'],
      setup_requires=setup_requires,
)
