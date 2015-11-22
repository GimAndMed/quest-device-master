#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty
from threading import RLock


class Resource:
    "Абстрактный класс ресурсов"
    __metaclass__ = ABCMeta

    NUM_LEDS = 32
    DEFAULT_VALUE = [0x0, 0x0, 0x0]

    def __init__(self):
        self.lock = RLock()

    @abstractmethod
    def setResource(self, resource): pass

    @abstractmethod
    def getResourse(self): pass

    @abstractmethod
    def changed(self):
        """ Абстрактный метод определения изменилось ли что-нибуь в данных
        или нет"""
        pass

    @abstractmethod
    def save(self): pass

    def equal(self, old, new):
        """Проверка равенства двух массивов"""
        if all(map(lambda a, b: a == b, old, new)):
            return True
        else:
            return False

    def set(self, resource):
        # захватываем блокировку
        self.lock.acquire()

        self.setResource(resource)
        # освобождаем блокировку
        self.lock.release()

    def get(self):
        self.lock.acquire()

        resource = self.getResource()

        self.lock.release()

        return resource

    def block(self):
        self.lock.acquire()

    def unblock(self):
        self.lock.release()
