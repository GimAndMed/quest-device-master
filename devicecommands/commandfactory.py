#!/usr/bin/python
# -*- coding: utf-8 -*-

from .commandcode import Command

# Общие команды
from .connectioncheck import ConnectionCheck
from .changespeed import ChangeSpeed

# Команды установки значений
from .setsimpleleds import SetSimpleLeds

from .setsmartoneleds import SetSmartOneLeds
from .setsmartquartetleds import SetSmartQuartetLeds
from .setsmartoctetleds import SetSmartOctetLeds
from .setsmartleds import SetSmartLeds

from .setlcd import SetLCD
from .setrelays import SetRelays

# Команды получения значений
from .getbuttons import GetButtons
from .getstuckbuttons import GetStuckButtons
from .getadc import GetADC
from .getencoders import GetEncoders
from .getsensor import GetSensor
from .getallstates import GetAllStates


class CommandFactory:

    def __init__(self):
        self.__debugMode = False

    def setDebugMode(self):
        self.__debugMode = True


    def createCommand(self, commandCode,
                      port=None, address=None, data=None, slave=None):
        # Общие команды
        if (Command.connectionCheck == commandCode):
            command = ConnectionCheck(port, address, data, slave)
        elif (Command.changeSpeed == commandCode):
            command = ChangeSpeed(port, address, data, slave)

        # Команды установки значений
        elif (Command.setSimpleLeds == commandCode):
            command = SetSimpleLeds(port, address, data, slave)
        elif (Command.setSmartOneLeds == commandCode):
            command = SetSmartOneLeds(port, address, data, slave)
        elif (Command.setSmartQuartetLeds == commandCode):
            command = SetSmartQuartetLeds(port, address, data, slave)
        elif (Command.setSmartOctetLeds == commandCode):
            command = SetSmartOctetLeds(port, address, data, slave)
        elif (Command.setSmartLeds == commandCode):
            command = SetSmartLeds(port, address, data, slave)
        elif (Command.setLCD == commandCode):
            command = SetLCD(port, address, data, slave)
        elif (Command.setRelays == commandCode):
            command = SetRelays(port, address, data, slave)

        # Команды получения значений
        elif (Command.getButtons == commandCode):
            command = GetButtons(port, address, data, slave)
        elif (Command.getStuckButtons == commandCode):
            command = GetStuckButtons(port, address, data, slave)
        elif (Command.getADC == commandCode):
            command = GetADC(port, address, data, slave)
        elif (Command.getEncoders == commandCode):
            command = GetEncoders(port, address, data, slave)
        elif (Command.getSensor == commandCode):
            command = GetSensor(port, address, data, slave)
        elif (Command.getAllStates == commandCode):
            command = GetAllStates(port, address, data, slave)

        if self.__debugMode:
            command.setDebugMode()

        return command
