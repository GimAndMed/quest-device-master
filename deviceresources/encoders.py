#!/usr/bin/python
# -*- coding: utf-8 -*-

from copy import copy
from resource import Resource


class Encoders(Resource):
    """Массив значений энкодеров
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
        self.encoders = self.DEFAULT_VALUE * self.NUM_ELEMENTS
        self.oldEncoders = self.DEFAULT_VALUE * self.NUM_ELEMENTS

    def setResource(self, encoders):
        if len(encoders) < self.NUM_ELEMENTS:
            self.encoders = encoders + [0] * \
                                        self.NUM_ELEMENTS - len(encoders)
        else:
            self.encoders = encoders[0: self.NUM_ELEMENTS]

    def getResource(self):
        retValue = copy(self.encoders)
        return retValue

    def save(self):
        pass

    def saveToOld(self, value):
        """Функция, предназначенная для сохранения статуса кнопок
        в другом массиве для последующего сравнения с обновлёнными
        значениями"""
        self.oldEncoders = value

    def changed(self):
        return not self.equal(self.oldEncoders, self.encoders)
