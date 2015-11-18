#!/usr/bin/python
# -*- coding: utf-8 -*-

from copy import copy
from resource import Resource


class SmartLeds(Resource):
    """Массив умных(RGB) светодиодов
        Доступ к массиву возможен функциями get и set
        При этом доступ реализован с блокировками

        Реализовано два массива.
        Массив значений, отправленных устройству (синхронизованный)
        Массив, доступный для чтения и записи клиентами.

        Перед отправкой команды устройству на установку значения
        умных светодиодов массивы сравниваются, для определения
        возможности посылки более легковесной команды устройству."""

    NUM_LEDS = 32
    DEFAULT_VALUE = [0x0, 0x0, 0x0]

    def __init__(self):
        Resource.__init__(self)
        # массив с которым работает клиент
        self.rgbLeds = self.DEFAULT_VALUE * self.NUM_LEDS

        # массив, что уже был отправлен устройству
        self.oldRgbLeds = self.DEFAULT_VALUE * self.NUM_LEDS

    def setResource(self, rgbArray):
        rgbArrayLen = len(rgbArray)
        rgbLedsLen = len(self.rgbLeds)

        # копируем
        if rgbArrayLen == rgbLedsLen:
            self.rgbLeds = copy(rgbArray)
        else:
            if rgbArrayLen > rgbLedsLen:
                lengthBarrier = rgbLedsLen
            else:
                lengthBarrier = rgbArrayLen

            for index in range(0, lengthBarrier):
                self.rgbLeds[index] = rgbArray[index]

    def getResourse(self):
        retValue = copy(self.rgbLeds)
        return retValue

    def save(self):
        """Сохраняем значение обновлённого массива
            функция используется после отправки
            команды устройству."""
        self.block()

        self.oldRgbLeds = copy(self.rgbLeds)

        self.unblock()

    def octetChanged(self):
        """Функция возвращает номер октета в
        котором изменились светодиоды, если он такой один"""
        pass

    def quartetChanged(self):
        """Функция возвращает номер квартета, в котором изменились
            светодиоды, если он такой один"""
        pass

    def oneChanged(self):
        """Функция возврщает номер светодиода, который изменился,
        если он такой один"""
        pass

    def changed(self):
        return not self.equal(self.oldLeds, self.leds)
