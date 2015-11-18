#!/usr/bin/python
# -*- coding: utf-8 -*-

from copy import copy
from resource import Resource


class SimpleLeds(Resource):
    """Массив простых светодиодов
        Доступ к массиву возможен функциями get и set
        При этом доступ реализован с блокировками

        Реализовано два массива.
        Массив значений, отправленных устройству (синхронизованный)
        Массив, доступный для чтения и записи клиентами.
    """

    NUM_LEDS = 80
    DEFAULT_VALUE = [0]

    def __init__(self):
        Resource.__init__(self)
        # массив с которым работает клиент
        self.leds = self.DEFAULT_VALUE * self.NUM_LEDS

        # массив, что уже был отправлен устройству
        self.oldLeds = self.DEFAULT_VALUE * self.NUM_LEDS

    def setResource(self, ledsArray):
        arrayLen = len(ledsArray)
        ledsLen = len(self.leds)

        # копируем
        if arrayLen == ledsLen:
            self.rgbLeds = copy(ledsArray)
        else:
            if arrayLen > ledsLen:
                lengthBarrier = ledsLen
            else:
                lengthBarrier = arrayLen

            for index in range(0, lengthBarrier):
                self.leds[index] = ledsArray[index]

    def getResourse(self):
        retValue = copy(self.leds)
        return retValue

    def save(self):
        """Сохраняем значение обновлённого массива
            функция используется после отправки
            команды устройству."""
        self.block()

        self.oldLeds = copy(self.leds)

        self.unblock()

    def changed(self):
        return not self.equal(self.oldLeds, self.leds)
