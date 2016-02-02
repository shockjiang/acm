#!/usr/bin/env python
import math

def do2(framelossrate, N=2.5, packetsize=1500.0):
    t = 1 - framelossrate/float(N)
    t = math.pow(t, 1/float(packetsize))
    t = 1 - t
    print t

def do(framelossrate, packetsize=1500.0):
    t = 1 - framelossrate
    t = math.pow(t, 1/float(packetsize))
    t = 1 - t
    print t


print "Case0"
for i in [0.01, 0.03, 0.05, 0.1]:
    do(i)

print "Case4"
for i in [0.01, 0.03, 0.05, 0.1]:
    do2(i)