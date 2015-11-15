#!/usr/bin/python
# -*- coding: utf-8 -*-

from devicecommand import DeviceCommand
from commandcode import Command


class SetSimpleLeds(DeviceCommand):
    """Выводится массив из 10 байт. Каждому биту соответствует
        свой светодиод (всего 80 светодиодов).
        Соответственно 1 – включен, 0 – выключен. Байты должны
        засылаться младшим байтом массива вперед. На плате светодиоды
        делятся на группы по 3и: «R», «G» «B» (номер в группе 0, 1 и 2
        соответственно). Группы считаются от 1.
        Для примера, 4ый бит 2го байта (считаем с 0) включит 20ый
        (опять таки считаем с 0) светодиод. Этот светодиод на плате
        имеет обозначение  «B» группы Led7. Обратная задача.
        Надо зажечь светодиод «R» группы Led22. Это 7 бит в 7 байте
        ((22-1)*3 + 0 «R» смещение = 63 бит)."""

    # код команды
    commandCode = Command.setSimpleLeds

    # кол-во целых байт данных в ответе
    numAnswerDataBytes = 0

    def packagingData(self, inOutPackage, data):
        """ Упаковываем данные для отправки """
        leds = self.slave.getSimpleLeds()

        # упаковываем данные
        for dataBayteId in range(0, len(leds), 8):
            dataByteList = leds[dataBayteId:dataBayteId + 8]

            # преобразуем массив битов в Байт
            # в старшем бите байта светодиод со старшим номером
            # print 'DataByteList: ', dataByteList
            dataByte = 0x00
            for dataBit in reversed(dataByteList):
                dataByte = dataByte << 1
                dataByte |= dataBit

            dataPackageBytes = self._createPackageDataBytes(dataByte)
            inOutPackage.extend(dataPackageBytes)

        return inOutPackage

    def parseData(self, data):
        """ В ответе данных нет: pass"""
        pass

    def saveDataInSlave(self, data):
        """ В ответе данных нет: pass"""
        pass
