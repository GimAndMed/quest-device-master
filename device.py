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
        self.relays = relays.Relays()
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

    # ЖКИ
    def getLcd(self):
        return self.lcd

    def setLcd(self, value):
        self.lcd.set(value)

    # Реле
    def getRelays(self):
        return self.relays

    def setRelays(self, value):
        self.relays.set(value)

    # Кнопки
    def getButtons(self):
        return self.buttons

    def getStuckButtons(self):
        return self.stuckButtons

    # Сенсорные кнопки
    def getSensors(self):
        return self.sensors

    # Умные светодиоды
    def getSmartLeds(self):
        return self.smartLeds

    def setSmartLeds(set, value):
        self.smartLeds.set(value)


    # Простые светодиоды
    def getSimpleLeds(self):
        return self.simpleLeds

    def setSimpleLeds(self, value):
        self.simpLeds.set(value)

    def executeCommands(self):
        """Функции устройства, выполняемые в потоке
        """
        # Получение состояния всех устройств
        self.sendCommand(Command.getAllStates)

        # Посылка команд установки значений
        if self.smartLeds.changed():
            self.sendSmartLeds()
        if self.relays.changed():
            self.sendRelays()
        if self.lcd.changed():
            self.sendLcd()
        if self.simpLeds.changed():
            self.sendSimpleLeds()

    def getName(self):
        return self.__name

    def getPort(self):
        return self.__portDescriptor

    def sendCommand(self, command, data=None):
        slave = self
        command = self.commandFactory.createCommand(
            command, self.__portDescriptor, self.__address, data, slave)
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

        block = self.smartLeds.getBlock()
        with block:
            # Определяем индексы светодиодов, которые были изменены.

            changedRgbIndexList = self.smartLeds.getChangeIdexes()

            octetIndex = self.smartLeds.octetChanged(changedRgbIndexList)
            quartetIndex = self.smartLeds.quartetChanged(
                changedRgbIndexList)
            oneRgbIndex = self.smartLeds.oneChanged(changedRgbIndexList)

            if octetIndex:
                data = [octetIndex]
                octetData = data.extend(data, self.smartLeds.getOctet(
                    octetIndex))
                sendStatus = self.sendCommand(
                    Command.setSmartOctetLeds, octetData)

            elif quartetIndex:
                data = [quartetIndex]
                quartetData = data.extend(data, self.smartLeds.getQuartet(
                    quartetIndex))
                sendStatus = self.sendCommand(
                    Command.setSmartQuartetLeds, quartetData)

            elif oneRgbIndex:
                data = [oneRgbIndex]
                oneRgbData = data.extend(data, self.smartLeds.getRgbLed(
                    oneRgbIndex))
                sendStatus = self.sendCommand(
                    Command.setSmartOneLeds, oneRgbData)
            else:
                sendStatus = self.sendCommand(Command.setSmartLeds,
                                              self.rgbLeds.get())
            # сохраняем отправленные на устройство значения
            if sendStatus:
                self.rgbLeds.save()

    def sendRelays(self):
        block = self.relays.getBlock()
        with block:
            sendStatus = self.sendCommand(
                Command.setRelays, self.relays.get())
            if sendStatus:
                self.relays.save()

    def sendLcd(self):
        block = self.lcd.getBlock()
        with block:
            sendStatus = self.sendCommand(
                Command.setLCD, self.lcd.get())
            if sendStatus:
                self.lcd.save()

    def sendSimpleLeds(self):
        block = self.simpleLeds.getBlock()
        with block:
            sendStatus = self.sendCommand(
                Command.setSimpleLeds, self.simpleLeds.get())
            if sendStatus:
                self.simpleLeds.save()
