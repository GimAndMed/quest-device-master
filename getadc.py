#!/usr/bin/python
# -*- coding: utf-8 -*-

from devicecommand import DeviceCommand, CommandConst


class GetADC(DeviceCommand):
    """Получить значения слайдеров и крутилок резистивных (каналы АЦП).
        В ответ 8 байт. 0 байт соответствует 0 каналу АЦП и т.д.
    """

    # код команды
    commandCode = CommandConst.getADC

    # кол-во целых байт данных в ответе
    numAnswerDataBytes = 8

    def packagingData(self, inOutPackage, data):
        """ Упаковываем данные для отправки
        Данных для упаковки get комманд - нет"""

        return inOutPackage

    def parseData(self, data):
        """Парсер АЦП данных
        В ответ 8 байт. 0 байт соответствует 0 каналу АЦП и т.д."""
        if len(data) != 8:
            # logPackage.debug("For command getADC data length\
            #  must be 8 bytes but we have: %d", len(data))
            return None
        return data

    def saveDataInSlave(self, data):
        """Если дескриптор слейва известен, то сохраняем данные,
        используя его интерфейс."""
        if self.__slave is not None:
            self.__slave.saveADC(data)
