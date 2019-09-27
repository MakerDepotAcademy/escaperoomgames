#!/usr/bin/env python3
import sys, re
with open(sys.argv[1], 'r') as f:
  s = re.sub(r'REPLACEME', sys.argv[2], f.read())
with open(sys.argv[1], 'w') as f:
  f.write(s)