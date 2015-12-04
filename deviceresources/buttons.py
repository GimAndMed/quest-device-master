#!/usr/bin/python
# -*- coding: utf-8 -*-

from copy import copy
from resource import Resource


class Buttons(Resource):
    """Массив кнопок
        Доступ к массиву возможен функцией get

        Реализовано два массива.
        Массив значений, отправленных устройству (синхронизованный)
        Массив, доступный для чтения и записи клиентами.
    """

    NUM_ELEMENTS = 18
    DEFAULT_VALUE = [0]

    def __init__(self):
        Resource.__init__(self)
        # массив с которым работает клиент
        self.buttons = self.DEFAULT_VALUE * self.NUM_ELEMENTS
        self.oldButtons = self.DEFAULT_VALUE * self.NUM_ELEMENTS

    def setResource(self, buttons):
        if len(buttons) < self.NUM_ELEMENTS:
            self.buttons = buttons + [0] * \
                                        self.NUM_ELEMENTS - len(buttons)
        else:
            self.buttons = buttons[0: self.NUM_ELEMENTS]

    def getResource(self):
        retValue = copy(self.buttons)
        return retValue

    def save(self):
        pass

    def saveToOld(self, value):
        """Функция, предназначенная для сохранения статуса кнопок
        в другом массиве для последующего сравнения с обновлёнными
        значениями"""
        self.oldButtons = value

    def changed(self):
        return not self.equal(self.oldButtons, self.buttons)

    def printResource(self):
        print("Buttons: \n")
        for index, value in enumerate(self.buttons):
            if (index % 2) == 0:
                print("\t")
            else
                print("\n")
            print("[{index}]: {value} ".format(index=index, value=value))
