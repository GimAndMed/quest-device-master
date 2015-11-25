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

    # Функции получения ресурсов устройства
    # Возвращаются объекты.
    def getAdc(self):
        return self.adc

    def getEncoders(self):
        return self.encoders

    def getLcd(self):
        return self.lcd

    def getRelays(self):
        return self.relays

    def getButtons(self):
        return self.buttons

    def getStuckButtons(self):
        return self.stuckButtons

    def getSensors(self):
        return self.sensors

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

    def getName(self):
        return self.__name

    def getPort(self):
        return self.__portDescriptor

    def sendCommand(self, command, data=None):
        command = self.CommandFactory.createCommand(
            command, self.__portDescriptor, self.__address, data, self)
        return command.execute()

    def sendGetAllState(self):
        """Посылка команды получения всех состояний устройства.
            Данные сохраняются внутри метода самой команды, посредством
            интерфейса устройства и интерфейса ресурсов"""
        allDeviceStates = self.sendCommand(Command.getAllStates)
        return allDeviceStates

    def sendSmartLeds(self):
        """ Отправка команды установки значений умных светодиодов
            1. Определяется какие значения были изменены.
            2. В соответствии с этим определяется какая команда будет
            отправлена устройству: установка октета, кваретета или
            одного светодиода.
            3. Отправка команды
            4. Сохранение текущих значений в массиве объекта
            светодиодов, хранящем значения, соответствующие тем, что были
            отправлены на устройство

            """

        # Определяем индексы светодиодов, которые были изменены.
        with self.lock:
            changedRgbIndexList = self.smartLeds.getChangeIdexes()

            octetIndex = self.smartLeds.octetChanged(changedRgbIndexList)
            quartetIndex = self.smartLeds.quartetChanged(
                changedRgbIndexList)
            oneRgbIndex = self.smartLeds.oneChanged(changedRgbIndexList)

            if octetIndex:
                data = [octetIndex]
                octetData = data.extend(data, self.smartLeds.getOctet(
                    octetIndex))
                self.sendCommand(Command.setSmartOctetLeds, octetData)

            elif quartetIndex:
                data = [quartetIndex]
                quartetData = data.extend(data, self.smartLeds.getQuartet(
                    quartetIndex))
                self.sendCommand(Command.setSmartQuartetLeds, quartetData)

            elif oneRgbIndex:
                data = [oneRgbIndex]
                oneRgbData = data.extend(data, self.smartLeds.getRgbLed(
                    oneRgbIndex))
                self.sendCommand(Command.setSmartOneLeds, oneRgbData)
            else:
                self.sendCommand(Command.setSmartLeds,
                                 self.rgbLeds.get())

    def sendRelays(self): pass

    def sendLcd(self): pass

    def sendSimpleLeds(self): pass
