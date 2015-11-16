#!/usr/bin/python
# -*- coding: utf-8 -*-

from devicecommands.commandfactory import CommandFactory
from devicecommands.commandcode import Command

import serial


def testAllGetFunction(port, address):
    commandFactory = CommandFactory()

    # GetFunction
    command = commandFactory.createCommand(Command.getButtons)
    command.init(port, address)
    connection = command.execute()

    command = commandFactory.createCommand(Command.getStuckButtons)
    command.init(port, address)
    connection = command.execute()

    command = commandFactory.createCommand(Command.getADC)
    command.init(port, address)
    connection = command.execute()

    command = commandFactory.createCommand(Command.getEncoders)
    command.init(port, address)
    connection = command.execute()

    command = commandFactory.createCommand(Command.getSensor)
    command.init(port, address)
    connection = command.execute()

    command = commandFactory.createCommand(Command.getAllStates)
    command.init(port, address)
    connection = command.execute()


def testAllSetFunction(port, address):

    commandFactory = CommandFactory()

    simpleLeds = [1, 0, 0, 1, 0, 1, 1, 0] * 10
    command = commandFactory.createCommand(Command.setSimpleLeds)
    command.init(port, address, simpleLeds)
    command.execute()

    oneSmartLed = [30, 0xfff, 0x0A0, 0xfaf]
    command = commandFactory.createCommand(Command.setSmartOneLeds)
    command.init(port, address, oneSmartLed)
    command.execute()

    octedSmartLed = [30] + [0xfff, 0x0A0, 0xfaf] * 8
    command = commandFactory.createCommand(Command.setSmartOctetLeds)
    command.init(port, address, octedSmartLed)
    command.execute()

    quartetSmartLed = [2] + [0xfff, 0x0A0, 0xfaf] * 4
    command = commandFactory.createCommand(Command.setSmartQuartetLeds)
    command.init(port, address, quartetSmartLed)
    command.execute()

    relays = [1, 0, 0, 1]
    command = commandFactory.createCommand(Command.setRelays)
    command.init(port, address, relays)
    command.execute()

    lcd = "hay Michael"
    command = commandFactory.createCommand(Command.setLCD)
    command.init(port, address, lcd)
    command.execute()

if __name__ == "__main__":

    ser = serial.Serial('/dev/pts/9',
                        timeout=1,
                        writeTimeout=0.1,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE)
    port = ser
    address = 1

    testAllGetFunction(port, address)

    testAllSetFunction(port, address)
