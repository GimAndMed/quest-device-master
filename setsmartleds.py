#!/usr/bin/python
# -*- coding: utf-8 -*-

from devicecommand import DeviceCommand, CommandConst


class SetSmartLeds(DeviceCommand):

    # код команды
    commandCode = CommandConst.setSmartLeds

    # кол-во целых байт данных в ответе
    numAnswerDataBytes = 0

    def packagingData(self, inOutPackage):
        """ Упаковываем данные для отправки.
            Создание пакета для установки значений умных светодиодов
            24 * 4 = 96 LEDs; 96 * 3  = 288 - элементов в списке data
             упаковываем данные
             Каждый светодиод описывается 3мя тетрадами (12 битами).
             Т.е. 12 бит – самого старшего светодиода, потом 12 бит
             предыдущего и т.д.
             Видно, что некоторые байты перехлестываются:
             старшая часть байта отвечает за один светодиод,
             младшая – за другой. В одной микросхеме 24 канала (24 светодиода).
             Таких микросхем 4е.
             Итого 4 микросхемы * 24 канала * 12 бит / 8 бит = 144 байта.
             144 байта * 2 = 288 байт данных в пакете + 2 crc + 3 st com
             = 293 байта в пакете
             меняем порядок тетрад
             H M L -> L M H"""
        data = self.__slave.getSmartLeds()

        reversed12BitData = []
        for brightness12Bit in data:
            # выделяем из 12 битового числа тетрады
            brightH = (brightness12Bit & 0xf00) >> 8
            brightM = (brightness12Bit & 0x0f0) >> 4
            brightL = (brightness12Bit & 0x00f)
            # сохраняем тетрады в обратном порядке,
            # чтобы правильно перевернуть, т.е.
            # старший светодиод шёл первым RGB RGB
            reversedBrightness = [brightL, brightM, brightH]
            reversed12BitData.extend(reversedBrightness)

        # делаем старший светодиод(последний) первым
        reversed12BitData = list(reversed(reversed12BitData))

        # Последовательно запихиваем тетрады в байт пакета
        dataByte = 0x00
        for tetradeH, tetradeL in zip(reversed12BitData[0::2],
                                      reversed12BitData[1::2]):
            tetradeH &= 0x0f
            tetradeL &= 0x0f
            dataByte = tetradeH << 4
            dataByte |= tetradeL
            dataPackageBytes = self._createPackageDataBytes(dataByte)
            inOutPackage.extend(dataPackageBytes)

        # считаем и упаковывае crc
        crcPackageBytes = self._createCRCPackageBytes(inOutPackage)
        inOutPackage.extend(crcPackageBytes)

        return inOutPackage

    def parseData(self, data):
        """ В ответе данных нет: pass"""
        pass

    def saveDataInSlave(self, data):
        """ В ответе данных нет: pass"""
        pass
