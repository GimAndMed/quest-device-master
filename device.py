#!/usr/bin/python
# -*- coding: utf-8 -*-

# Импортируем ресурсы - объекты, содержащие данные платы
# соответствующего типа.
from deviceresources import adc, encoders, lcd
from deviceresources import relays, sensors, simpleleds, smartleds
from deviceresources import buttons, stuckbuttons

# Импортируем фабрику команд
from devicecommands.commandfactory import CommandFactory
from devicecommands.commandcode import Command


class Device:
    """Устройство. Предоставляет доступ к данным подключённой платы.
    """

    def __init__(self, address, portDescriptor, name=None):
        self.__address = address
        self.__portDescriptor = portDescriptor
        self.__name = name

        # Создаём фабрику команд
        self.commandFactory = CommandFactory()

        # создаём реcурсы
        self.adc = adc.Adc()
        self.encoders = encoders.Encoders()
        self.lcd = lcd.Lcd()
        self.relays = relays.Relays
        self.sensors = sensors.Sensors()
        self.simpLeds = simpleleds.SimpleLeds()
        self.smartLeds = smartleds.SmartLeds()
        self.buttons = buttons.Buttons()
        self.stuckButtons = stuckbuttons.StuckButtons()

    def executeCommands(self):
        self.sendCommand(Command.getAllStates)

        if self.smartLeds.changed():
            self._sendSmartLeds()
        if self.relays.changed():
            self._sendRelays()
        if self.lcd.changed():
            self._sendLcd()
        if self.simpLeds.changed():
            self._sendSimpleLeds()

    def sendCommand(self, command, data=None):
        command = self.CommandFactory.createCommand(
            command, self.__portDescriptor, self.__address, data, self)
        command.execute()

    def _sendSmartLeds(self): pass

    def _sendRelays(self): pass

    def _sendLcd(self): pass

    def _sendSimpleLeds(self): pass
