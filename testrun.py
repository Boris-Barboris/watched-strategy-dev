#!/usr/bin/python2.7

import sys

from consolidation_tests import *

cases = [
    case_simple1,           #0
    case_uniform_cpu,       #1
    case_uniform_ram,       #2
    case_isolated_simple,   #3
    ]

if len(sys.argv) > 1:
    index = int(sys.argv[1])
else:
    index = 0
func = cases[index]
print 'running function ' + func.__name__
func()
