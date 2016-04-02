#!/usr/bin/python
# -*- coding: utf-8 -*-

# socat -d -d pty,raw,echo=0 pty,raw,echo=0
# socat PTY,link=./ptyp1,b9600 PTY,link=./ptyp2,b9600

# from devicemaster import DeviceMaster
from ..devicemaster import DeviceMaster
from time import sleep
import argparse

import os
import sys

def clear():
    os.system('cls' if os.name=='nt' else 'clear')


RED = [0xfff, 0x0, 0x0]
GREEN = [0x0, 0xfff, 0x0]
BLUE = [0x0, 0x0, 0xfff]


def setLedValue(leds, id, color):
    leds[id * 3 + 0] = color[0]
    leds[id * 3 + 1] = color[1]
    leds[id * 3 + 2] = color[2]


def testSmartLeds(slave):
    smartLeds = slave.getSmartLeds().get()
    print("Change ALL")
    for index in range(32):
        setLedValue(smartLeds, index, RED)
    slave.setSmartLeds(smartLeds)
    raw_input("Press Enter to continue...")
    print("Change ONE")
    for index in [4]:
        setLedValue(smartLeds, index, GREEN)
    slave.setSmartLeds(smartLeds)

    raw_input("Press Enter to continue...")

    # print("Change 2")
    # for index in range(2):
    #     setLedValue(smartLeds, index, BLUE)
    # slave.setSmartLeds(smartLeds)

    print("Change 4 Blue")
    for index in range(4):
        setLedValue(smartLeds, index, BLUE)
    slave.setSmartLeds(smartLeds)

    raw_input("Press Enter to continue...")

    print("Change 6")
    for index in range(6):
        setLedValue(smartLeds, index, [0x00, 0x00, 0x00])
    slave.setSmartLeds(smartLeds)
    raw_input("Press Enter to continue...")


def printAllStates(master, slave):
    print("Buttons: ", master.getButtons(slave).get())
    print("Adc: ", master.getAdc(slave).get())
    print("Encoders: ", master.getEncoders(slave).get())
    print("Lcd: ", master.getLcd(slave).get())
    print("Relays: ", master.getRelays(slave).get())
    print("Sensors: ", master.getSensors(slave).get())
    print("SimpleLeds: ", master.getSimpleLeds(slave).get())
    print("SmartLeds: ", master.getSmartLeds(slave).get())


if __name__ == "__main__":
    pass
    parser = argparse.ArgumentParser(description="Get visual information about buttons, adc and encoders for given slave")
    parser.add_argument("slave_id", help="""Enter 0 for print all devices\n
            enter 1 for hallwayPazzle only\n
            enter 2 for CB_SLAVE_1
            enter 3 for CB_SLAVE_2""",
            type=int)
    if len(sys.argv) == 1:
        # print("Usage {}".format(parser.usage));
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    slave_id = args.slave_id

    master = DeviceMaster()

    # portDestination = os.path.expanduser('~') + '/ptyp2'
    #portDestination = "/dev/ttyUSB0"
    #portDestination = "/dev/ttyUSB0"
    port_CB_SLAVE_1 = "COM5"
    port_CB_SLAVE_2 = "COM4"
    hallwayPuzzles = master.addSlave("hallwayPuzzles", "COM3", 1, boudrate=5)
    CB_SLAVE_2 = master.addSlave("CB_SLAVE_2", port_CB_SLAVE_2, 1, boudrate=5)
    CB_SLAVE_1 = master.addSlave("CB_SLAVE_1", port_CB_SLAVE_1, 2, boudrate=5)
    master.start()
    while True:

        if slave_id == 1 or slave_id == 0:
            print("hallwayPuzzles: First and second Monitor")
            master.getButtons(hallwayPuzzles).printResource()
            master.getAdc(hallwayPuzzles).printResource()
            master.getEncoders(hallwayPuzzles).printResource()

        if slave_id == 2 or slave_id == 0:
            print("CB_SLAVE_1: First and second Monitor")
            master.getButtons(CB_SLAVE_1).printResource()
            master.getAdc(CB_SLAVE_1).printResource()
            master.getEncoders(CB_SLAVE_1).printResource()
        # # printAllStates(master, slave)
        # # raw_input("Press Enter to continue...")

        if slave_id == 3 or slave_id == 0:
            print("\n\nCB_SLAVE_2: 3 and 4 Monitor")
            master.getButtons(CB_SLAVE_2).printResource()
            master.getAdc(CB_SLAVE_2).printResource()
            master.getEncoders(CB_SLAVE_2).printResource()
        #master.getRelays(CB_SLAVE_2).printResource()

        if slave_id == 0:
            raw_input("Press Enter to refresh...")

        sleep(0.1)
        clear()
