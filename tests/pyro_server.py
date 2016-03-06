#!/usr/bin/python
# -*- coding: utf-8 -*-

# socat -d -d pty,raw,echo=0 pty,raw,echo=0
# socat PTY,link=./ptyp1,b9600 PTY,link=./ptyp2,b9600

from ..devicemaster import DeviceMaster

from time import sleep

import os

# http://pythonhosted.org/Pyro/

if __name__ == "__main__":
    pass
    os.environ["DEVICE_DEBUG"] = "1"
    master = DeviceMaster()

    port_CB_SLAVE_1 = "COM5"
    port_CB_SLAVE_2 = "COM4"
    CB_SLAVE_2 = master.addSlave("CB_SLAVE_2", port_CB_SLAVE_2, 1, boudrate=5)
    CB_SLAVE_1 = master.addSlave("CB_SLAVE_1", port_CB_SLAVE_1, 2, boudrate=5)
    master.start()

    while True:
        print("CB_SLAVE_1: ")
        master.getButtons(CB_SLAVE_1).printResource()
        master.getAdc(CB_SLAVE_1).printResource()
        sleep(2)

