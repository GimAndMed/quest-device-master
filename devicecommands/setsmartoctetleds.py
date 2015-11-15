#!/usr/bin/python
# -*- coding: utf-8 -*-

from devicecommand import DeviceCommand
from commandcode import Command


class SetSmartOctetLeds(DeviceCommand):
    """Установить выборочное значение 8ми умных светодиодов.
        В данных 1н байт номер драйвера (0-3) и 36 байт значения
        светодиодов по 12 бит на канал светодиода.
        При этом номер драйвера 0 управляет  LED1 — LED8,
         номер 1 - LED9 — LED16...
        В данных 37 байт
    """
    # код команды
    commandCode = Command.setSmartOctetLeds

    # кол-во целых байт данных в ответе
    numAnswerDataBytes = 0

    def packagingData(self, inOutPackage, data):
        """ Упаковываем данные для отправки.
            Всё как в отправке большого массива.
            Только первый байт данных - номер половины драйвера.
        """
        # Вставляем в пакет номер ПОЛОВИНЫ драйвера.
        # При этом 0 управляет  LED1 — LED4, номер 1 - LED5 — LED8...
        dataPackageBytes = self._createPackageDataBytes(data[0])
        inOutPackage.extend(dataPackageBytes)

        dataPackage = self._packedInDataSmartSelectiveLEDs(data[1:])
        inOutPackage.extend(dataPackage)

        return inOutPackage

    def _packedInDataSmartSelectiveLEDs(self, data):
        """Упаковываем только данные RGB светодиодов, больше 1"""
        package = []
        reversed12BitData = []
        for brightness12Bit in data:
            # выделяем из 12 битового числа тетрады
            brightH = (brightness12Bit & 0xf00) >> 8
            brightM = (brightness12Bit & 0x0f0) >> 4
            brightL = (brightness12Bit & 0x00f)
            # сохраняем тетрады в обратном порядке, чтобы правильно перевернуть
            reversedBrightness = [brightL, brightM, brightH]
            # reversedBrightness = [brightH, brightM, brightL]
            reversed12BitData.extend(reversedBrightness)

        # делаем старший светодиод(последний) первым
        reversed12BitData = list(reversed(reversed12BitData))
        # reversed12BitData = list(reversed12BitData)

        # Последовательно запихиваем тетрады в байт пакета
        dataByte = 0x00
        for tetradeH, tetradeL in zip(reversed12BitData[0::2],
                                      reversed12BitData[1::2]):
            tetradeH &= 0x0f
            tetradeL &= 0x0f
            dataByte = tetradeH << 4
            dataByte |= tetradeL
            dataPackageBytes = self._createPackageDataBytes(dataByte)
            package.extend(dataPackageBytes)

        return package

    def parseData(self, data):
        """ В ответе данных нет: pass"""
        pass

    def saveDataInSlave(self, data):
        """ В ответе данных нет: pass"""
        pass
