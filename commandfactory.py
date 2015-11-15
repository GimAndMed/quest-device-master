#!/usr/bin/python
# -*- coding: utf-8 -*-

from devicecommand import CommandConst

# Общие команды
from connectioncheck import ConnectionCheck
from changespeed import ChangeSpeed

# Команды установки значений
from setsimpleleds import SetSimpleLeds

from setsmartoneleds import SetSmartOneLeds
from setsmartquartetleds import SetSmartQuartetLeds
from setsmartoctetleds import SetSmartOctetLeds
from setsmartleds import SetSmartLeds

from setlcd import SetLCD
from setrelays import SetRelays

# Команды получения значений
from getbuttons import GetButtons
from getstuckbuttons import GetStuckButtons
from getadc import GetADC
from getencoders import GetEncoders
from getsensor import GetSensor
from getallstates import GetAllStates


class CommandFactory:

    def __init__(self):
        pass

    def createCommand(self, commandCode,
                      port=None, address=None, data=None, slave=None):
        # Общие команды
        if (CommandConst.connectionCheck == commandCode):
            command = ConnectionCheck(port, address, data, slave)
        elif (CommandConst.changeSpeed == commandCode):
            command = ChangeSpeed(port, address, data, slave)

        # Команды установки значений
        elif (CommandConst.setSimpleLeds == commandCode):
            command = SetSimpleLeds(port, address, data, slave)
        elif (CommandConst.setSmartOneLeds == commandCode):
            command = SetSmartOneLeds(port, address, data, slave)
        elif (CommandConst.setSmartQuartetLeds == commandCode):
            command = SetSmartQuartetLeds(port, address, data, slave)
        elif (CommandConst.setSmartOctetLeds == commandCode):
            command = SetSmartOctetLeds(port, address, data, slave)
        elif (CommandConst.setSmartLeds == commandCode):
            command = SetSmartLeds(port, address, data, slave)
        elif (CommandConst.setLCD == commandCode):
            command = SetLCD(port, address, data, slave)
        elif (CommandConst.setRelays == commandCode):
            command = SetRelays(port, address, data, slave)

        # Команды получения значений
        elif (CommandConst.getButtons == commandCode):
            command = GetButtons(port, address, data, slave)
        elif (CommandConst.getStuckButtons == commandCode):
            command = GetStuckButtons(port, address, data, slave)
        elif (CommandConst.getADC == commandCode):
            command = GetADC(port, address, data, slave)
        elif (CommandConst.getEncoders == commandCode):
            command = GetEncoders(port, address, data, slave)
        elif (CommandConst.getSensor == commandCode):
            command = GetSensor(port, address, data, slave)
        elif (CommandConst.getAllStates == commandCode):
            command = GetAllStates(port, address, data, slave)

        return command
