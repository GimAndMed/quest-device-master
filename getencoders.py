#!/usr/bin/python
# -*- coding: utf-8 -*-

from devicecommand import DeviceCommand, CommandConst


class GetEncoders(DeviceCommand):
    """Получить значение энкодеров.
       В ответ 8 байт (по 2а байта на крутилку). Значения LE.
       0 счетчик (16 бит) соответствует 0 крутилке.
    """

    # код команды
    commandCode = CommandConst.getEncoders

    # кол-во целых байт данных в ответе
    numAnswerDataBytes = 8

    def packagingData(self, inOutPackage, data):
        """ Упаковываем данные для отправки
        Данных для упаковки get комманд - нет"""

        return inOutPackage

    def parseData(self, data):
        """Парсер данных энкодеров
        В ответ 8 байт (по 2а байта на крутилку). Значения LE.
        0 счетчик (16 бит) соответствует 0 крутилке."""

        if len(data) != 8:
            # logPackage.debug("For command getEncoder data length\
            #  must be 8 bytes but we have: %d", len(data))
            return None
        encoderList = []
        for index in range(0, 8, 2):
            # значения Little-endian!
            encoderValue = (data[index + 1] << 8) | (data[index])
            encoderList.append(encoderValue)
        return encoderList

    def saveDataInSlave(self, data):
        """Если дескриптор слейва известен, то сохраняем данные,
        используя его интерфейс."""
        if self.__slave is not None:
            self.__slave.saveEncoders(data)
