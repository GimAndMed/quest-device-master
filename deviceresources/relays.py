#!/usr/bin/python
# -*- coding: utf-8 -*-

from copy import copy
from .resource import Resource


class Relays(Resource):
    """Массив реле
        Доступ к массиву возможен функциями get и set
        При этом доступ реализован с блокировками

        Реализовано два массива.
        Массив значений, отправленных устройству (синхронизованный)
        Массив, доступный для чтения и записи клиентами.
    """

    NUM_RELAYS = 4
    DEFAULT_VALUE = [0]

    def __init__(self):
        Resource.__init__(self)
        # super(Resource, self).__init__()
        # массив с которым работает клиент
        self.relays = self.DEFAULT_VALUE * self.NUM_RELAYS

        # массив, что уже был отправлен устройству
        self.oldRelays = self.DEFAULT_VALUE * self.NUM_RELAYS

    def setResource(self, relays):

        if len(relays) < self.NUM_RELAYS:
            self.relays = relays + [0] * (self.NUM_RELAYS - len(relays))
        else:
            self.relays = relays[0: self.NUM_RELAYS]

    def getResource(self):
        retValue = copy(self.relays)
        return retValue

    def save(self):
        """Сохраняем значение обновлённого массива
            функция используется после отправки
            команды устройству."""
        self.block()

        self.oldRelays = copy(self.relays)

        self.unblock()

    def changed(self):
        return not self.equal(self.oldRelays, self.relays)
