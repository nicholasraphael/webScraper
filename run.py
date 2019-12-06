'''Helper script for running multiple tickers
'''

import sys
import time
from subprocess import Popen

import sys
tickers = sys.stdin.readlines()

for line in tickers:
    if line and line != '\n':
        arg = str(line).strip()
        Popen(["python", "./takehome.py", arg])
        time.sleep(2)

sys.exit()
