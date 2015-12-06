#!/usr/bin/python
# -*- coding: utf-8 -*-

from copy import copy
from .resource import Resource


class Lcd(Resource):
    """Массив ЖКИ
        Доступ к массиву возможен функциями get и set
        При этом доступ реализован с блокировками

        Реализовано два массива.
        Массив значений, отправленных устройству (синхронизованный)
        Массив, доступный для чтения и записи клиентами.
    """

    NUM_ELEMENTS = 80
    DEFAULT_VALUE = [0]

    def __init__(self):
        Resource.__init__(self)
        # массив с которым работает клиент
        self.lcd = self.DEFAULT_VALUE * self.NUM_ELEMENTS

        # массив, что уже был отправлен устройству
        self.oldLcd =  '' * self.NUM_ELEMENTS

    def setResource(self, lcd):

        if len(lcd) < self.NUM_ELEMENTS:
            self.lcd = lcd + ' ' * (self.NUM_ELEMENTS - len(lcd))
        else:
            self.lcd = lcd[0: self.NUM_ELEMENTS]

    def getResource(self):
        retValue = copy(self.lcd)
        return retValue

    def save(self):
        """Сохраняем значение обновлённого массива
            функция используется после отправки
            команды устройству."""
        self.block()

        self.oldLcd = copy(self.lcd)

        self.unblock()

    def changed(self):
        return not self.equal(self.oldLcd, self.lcd)
