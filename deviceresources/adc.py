#!/usr/bin/python
# -*- coding: utf-8 -*-

from copy import copy
from resource import Resource


class Adc(Resource):
    """Массив значений АЦП
        Доступ к массиву возможен функцией get

        Реализовано два массива.
        Массив значений, отправленных устройству (синхронизованный)
        Массив, доступный для чтения и записи клиентами.
    """

    NUM_ELEMENTS = 8
    DEFAULT_VALUE = [0]

    def __init__(self):
        Resource.__init__(self)
        # массив с которым работает клиент
        self.adc = self.DEFAULT_VALUE * self.NUM_ELEMENTS
        self.oldAdc = self.DEFAULT_VALUE * self.NUM_ELEMENTS

    def setResource(self, adc):
        if len(adc) < self.NUM_ELEMENTS:
            self.adc = adc + [0] * (self.NUM_ELEMENTS - len(adc))
        else:
            self.adc = adc[0: self.NUM_ELEMENTS]

    def getResource(self):
        retValue = copy(self.adc)
        return retValue

    def save(self):
        pass

    def saveToOld(self, value):
        """Функция, предназначенная для сохранения статуса кнопок
        в другом массиве для последующего сравнения с обновлёнными
        значениями"""
        self.oldAdc = value

    def changed(self):
        return not self.equal(self.oldAdc, self.adc)
