#!/usr/bin/python2.7

import sys
from inspect import getmembers, isfunction

import consolidation_tests

cases = [o for o in getmembers(consolidation_tests, isfunction)]

if len(sys.argv) > 1:
    index = int(sys.argv[1])
else:
    index = 0
cases[index][1]()
