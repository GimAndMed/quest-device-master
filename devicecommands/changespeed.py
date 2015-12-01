#!/usr/bin/python
# -*- coding: utf-8 -*-

from devicecommand import DeviceCommand
from commandcode import Command
from time import sleep


class ChangeSpeed(DeviceCommand):
    """
        Установить скорость обмена.
        При включении платы скорость всегда 9600 бит/с. 1 байт данных:
        0 - 9 600
        1 - 14 400
        2 – 19 200
        3 – 28 800
        4 – 38 400
        5 – 57 600
        6 – 76 800
        7 – 115 200
        Ответ придет на новой скорости, но, скорее всего,
        его поймать не получится
            (надо довольно быстро переключить скорость).
    """

    # код команды
    commandCode = Command.changeSpeed

    # кол-во целых байт данных в ответе
    numAnswerDataBytes = 0

    # список скоростей
    baudrateList = [9600, 14400, 19200, 28800,
                    38400, 57600, 76800, 115200]

    def packagingData(self, inOutPackage, data):
        """ Упаковываем данные для отправки """

        dataPackageBytes = self._createPackageDataBytes(data)
        inOutPackage.extend(dataPackageBytes)

        return inOutPackage

    # переопределяем функцию отправки, для смены скорости
    def send(self, package):
        numBytesSend = self.portDescriptor.write(str(bytearray(package)))

        self._setNewSpeed()

        return numBytesSend

    def _setNewSpeed(self):
        speedID = self.data
        if speedID < 0 or speedID >= len(self.baudrateList):
            print "Speed do not changed - wrong speedID: ", speedID
            return

        oldBaudrate = self.portDescriptor.baudrate
        print "oldBaudrate: ", oldBaudrate, " New baudrate: ", self.baudrateList[speedID], " speedID: ", speedID
        if oldBaudrate == self.baudrateList[speedID]:
            print "New speed is equal to old; do not change speed"
            return

        self.portDescriptor.flush()
        sleep(1)

        self.portDescriptor.baudrate = self.baudrateList[speedID]
        self.portDescriptor.close()
        sleep(1)
        self.portDescriptor.open()
        print "Speed changed from {0} to {1}: ".format(
            oldBaudrate, self.baudrateList[speedID])
        sleep(1)

    def parseData(self, data):
        """ В ответе данных нет: pass"""
        pass

    def saveDataInSlave(self, data):
        """ В ответе данных нет: pass"""
        pass
