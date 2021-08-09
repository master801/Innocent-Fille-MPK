#!/usr/bin/env python3

import sys

if sys.platform == 'linux':
    FP_SEP = '/'
    pass
else:
    FP_SEP = '\\'
    pass

MODE_EXTRACT = 'e'
MODE_CREATE = 'c'
