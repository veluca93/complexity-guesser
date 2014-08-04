#!/usr/bin/env python2

import sys

import complexity_guesser

usage = "Usage: %s <variables file> <times file>" % sys.argv[0]

if len(sys.argv) < 3:
    print >> sys.stderr, usage
    exit(1)

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

lines = open(sys.argv[1]).readlines()
sizes = [map(int, l.split()) for l in lines[1:]]
varnames = lines[0].strip().split()

lines = open(sys.argv[2]).readlines()
data = [(tuple(sizes[i]), float(lines[i])) for i in xrange(len(lines))
        if isfloat(lines[i])]

print complexity_guesser.guess(varnames, data)
