#!/usr/bin/python
# -*- coding: utf-8 -*-

from devicecommand import DeviceCommand, CommandConst
from time import sleep


class changeSpeed(DeviceCommand):
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
    commandCode = CommandConst.changeSpeed

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
        numBytesSend = self.__portDescriptor.write(package)

        self._setNewSpeed()

        return numBytesSend

    def _setNewSpeed(self):
        speedID = self.__data
        if speedID < 0 or speedID >= len(self.baudrateList):
            print "Speed do not changed - wrong speedID: ", speedID
            return
        self.__portDescriptor.flush()
        sleep(1)
        oldBaudrate = self.__portDescriptor.baudrate
        self.__portDescriptor.baudrate = self.baudrateList[speedID]
        self.__portDescriptor.close()
        sleep(1)
        self.__portDescriptor.open()
        print "Speed changed from {0} to {1}: ".format(
            self.baudrateList[speedID], oldBaudrate)
        sleep(1)

    def parseData(self, data):
        """ В ответе данных нет: pass"""
        pass

    def saveDataInSlave(self, data):
        """ В ответе данных нет: pass"""
        pass
