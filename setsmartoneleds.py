#!/usr/bin/python
# -*- coding: utf-8 -*-

from devicecommand import DeviceCommand, CommandConst


class SetSmartOneLeds(DeviceCommand):
    """Установить значение 1го умного светодиода.
        В данных номер светодиода (0 — 31). 0 соответствует
        подписанному на плате 1му светодиоду.
        Далее 2 байта яркости на R канал, 2а байта на G, 2а байта на B.
        Из 2х байт используется только младшие 12 бит.
    """
    # код команды
    commandCode = CommandConst.setSmartOneLeds

    # кол-во целых байт данных в ответе
    numAnswerDataBytes = 2

    def packagingData(self, inOutPackage, data):
        """ Упаковываем данные для отправки.
            Создание пакета для установки значений одного умного
            светодиодов
            Светодиод описывается 3мя тетрадами (12 битами).
            Два байта данных на одни светодиод
        """
        # Вставляем в пакет номер RGB светодиода от 0 до 31
        dataPackageBytes = self._createPackageDataBytes(data[0])
        inOutPackage.extend(dataPackageBytes)

        dataPackage = self._packedInDataSmartOneLEDs(data[1:])
        inOutPackage.extend(dataPackage)

        # считаем и упаковывае crc
        crcPackageBytes = self._createCRCPackageBytes(inOutPackage)
        inOutPackage.extend(crcPackageBytes)

        return inOutPackage

    def _packedInDataSmartOneLEDs(self, data):
        """Упаковываем данные светодиода. По два байта на R, G и B"""
        package = []
        # print "\n\nData: ", data, "\n\n"
        # bytesList = []
        for twoBytes in data:
            byteH = (twoBytes & 0xff00) >> 8
            dataPackageBytes = self._createPackageDataBytes(byteH)
            package.extend(dataPackageBytes)

            byteL = (twoBytes & 0xff)

            dataPackageBytes = self._createPackageDataBytes(byteL)
            package.extend(dataPackageBytes)
        return package

    def parseData(self, data):
        """ В ответе данных нет: pass"""
        pass

    def saveDataInSlave(self, data):
        """ В ответе данных нет: pass"""
        pass
