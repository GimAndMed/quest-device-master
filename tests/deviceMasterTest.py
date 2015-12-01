#!/usr/bin/python
# -*- coding: utf-8 -*-

# socat -d -d pty,raw,echo=0 pty,raw,echo=0
# socat PTY,link=./ptyp1,b9600 PTY,link=./ptyp2,b9600

from ..devicemaster import DeviceMaster
from ..devicemaster import DeviceMaster
from time import sleep

import os

if __name__ == "__main__":
    pass
    master = DeviceMaster()

    portDestination = os.path.expanduser('~') + '/ptyp2'
    slave = master.addSlave("testSlave", portDestination, 1, boudrate=0)

    while True:
        relays = slave.getRelays()
        print relays.get()
        # relays.set([1,0,0,1])
        # slave.setRelays([1, 0, 0, 1])
        sleep(5)
        # slave.setRelays([1,0,0,1])
        relays.set([1,0,0,1])
        sleep(5)
