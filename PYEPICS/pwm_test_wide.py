#!/usr/bin/python

'''
configures PWM on UUT

'''

import epics
import time
import sys
import os

UUT=os.getenv('IOC_HOST')
D_AQB="d2" # default to site 1
SITE=5

if len(sys.argv) == 3:
    UUT = sys.argv[1]
    D_AQB = format("d{}".format(int(sys.argv[2])+1))

root = "{}:{}:PPW".format(UUT, SITE)

def pvput(suffix, value):
    name = root+suffix
    print("{} {}".format(name, value))
    epics.caput(name, value, wait=True)

dioen = "{}:{}:DIO:ENABLE".format(UUT, SITE)
clkdiv = "{}:{}:CLKDIV".format(UUT, SITE)
countclr = "{}:{}:DIO:ENABLE:clr".format(UUT, SITE)

epics.caput(dioen, 0, wait=True)

epics.caput(clkdiv, 1, wait=True)
epics.caput(countclr, 1, wait=True)


for dx in (1, 2, 3, 4, 5, 6):
    pvput(":{}:TRG".format(dx),        "TRG_BUS" if dx==2 else "IM_BUS")    
    pvput(":{}:TRG:DX".format(dx),     "d0" if dx==2 else D_AQB)    
    pvput(":{}:TRG:SENSE".format(dx),  "rising")

    pvput(":{}:REPS".format(dx),       20 if dx==2 else 1)

    pvput(":{}:PULSE".format(dx),      "INIT_LO")
    pvput(":{}:PULSE:DELAY".format(dx),   1)
    pvput(":{}:PULSE:WIDTH".format(dx),   20e-6 if dx==2 else 4e-6)
    pvput(":{}:PULSE:PERIOD".format(dx), 4e-3 if dx==2 else 6e-6)

        
epics.caput(dioen, 1)

