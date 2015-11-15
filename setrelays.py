#!/usr/bin/python
# -*- coding: utf-8 -*-

from devicecommand import DeviceCommand, CommandConst


class SetRelays(DeviceCommand):
    """Установить значение реле:
        Бит 4 – реле 1.
        Бит 5 – реле 2.
        Бит 6 – реле 3.
        Бит 7 – реле 4.
        Остальные биты не обрабатываются.
    """

    # код команды
    commandCode = CommandConst.setRelays

    # кол-во целых байт данных в ответе
    numAnswerDataBytes = 0

    def packagingData(self, inOutPackage, data):
        """ Упаковываем данные для отправки """

        # упаковываем данные
        for dataBayteId in range(0, len(data), 8):  # = [0]
            dataByteList = data[dataBayteId:dataBayteId + 8]
            # преобразуем массив битов в Байт
            # бит 4 - реле 1; бит 5 - реле 2
            # Биты байта в данных: от старшего к младшему

            # поэтому разворачиваем значения в обратном порядке
            # запихиваем в байт побитно, каждый раз сдвигая влево
            dataByte = 0x00
            reversedData = reversed(dataByteList)
            for dataBit in reversedData:
                dataByte = dataByte << 1
                dataByte |= dataBit
            dataByte = dataByte << 4

            dataPackageBytes = self._createPackageDataBytes(dataByte)
            inOutPackage.extend(dataPackageBytes)

        return inOutPackage

    def parseData(self, data):
        """ В ответе данных нет: pass"""
        pass

    def saveDataInSlave(self, data):
        """ В ответе данных нет: pass"""
        pass
