#!/usr/bin/python
# -*- coding: utf-8 -*-

from .devicecommand import DeviceCommand
from .commandcode import Command


class GetSensor(DeviceCommand):
    """Получить значения сенсорных кнопок.
    В ответ 2а байта – попугаи сенсорной кнопки 1 и попугаи
    сенсорной кнопки 2.
    """

    # код команды
    commandCode = Command.getSensor

    # кол-во целых байт данных в ответе
    numAnswerDataBytes = 2

    def packagingData(self, inOutPackage, data):
        """ Упаковываем данные для отправки
        Данных для упаковки get комманд - нет"""

        return inOutPackage

    def parseData(self, data):
        """ Парсер значений сенсорных кнопок
        Значения от 0 до 255 для каждой кнопки, их вроде 2,
            так что считаем что два байта, но не будем пока ограничивать
        """

        return data

    def saveDataInSlave(self, data):
        """Если дескриптор слейва известен, то сохраняем данные,
        используя его интерфейс."""
        if self.slave is not None:
            self.slave.saveSensor(data)
