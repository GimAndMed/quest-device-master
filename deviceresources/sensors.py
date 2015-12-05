#!/usr/bin/python
# -*- coding: utf-8 -*-

from copy import copy
from .resource import Resource


class Sensors(Resource):
    """Массив значений энкодеров
        Доступ к массиву возможен функцией get

        Реализовано два массива.
        Массив значений, отправленных устройству (синхронизованный)
        Массив, доступный для чтения и записи клиентами.
    """

    NUM_ELEMENTS = 2
    DEFAULT_VALUE = [0]

    def __init__(self):
        Resource.__init__(self)
        # массив с которым работает клиент
        self.elements = self.DEFAULT_VALUE * self.NUM_ELEMENTS
        self.oldElements = self.DEFAULT_VALUE * self.NUM_ELEMENTS

    def setResource(self, elements):
        if len(elements) < self.NUM_ELEMENTS:
            self.elements = elements + [0] * \
                                        self.NUM_ELEMENTS - len(elements)
        else:
            self.elements = elements[0: self.NUM_ELEMENTS]

    def getResource(self):
        retValue = copy(self.elements)
        return retValue

    def save(self):
        pass

    def saveToOld(self, value):
        """Функция, предназначенная для сохранения статуса кнопок
        в другом массиве для последующего сравнения с обновлёнными
        значениями"""
        self.odlElements = value

    def changed(self):
        return not self.equal(self.oldElements, self.elements)
