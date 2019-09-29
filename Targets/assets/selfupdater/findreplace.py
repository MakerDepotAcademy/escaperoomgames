#!/usr/bin/env python3
import sys, re, os
with open(sys.argv[1], 'r') as f:
  s = re.sub(r'REPLACEME', sys.argv[2], f.read())
  s = re.sub(r'REPLACEDIR', os.path.dirname(sys.argv[2]), s)
with open(sys.argv[1], 'w') as f:
  f.write(s)