#!/usr/bin/python
# -*- coding: utf-8 -*-

from copy import copy
from .resource import Resource

# итераторы для двух объектов сразу
from itertools import count
try:
    # Python 2.7
    from itertools import izip
except ImportError:
    # python3
    izip = zip


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
        self.oldRgbLeds = [1, 1, 1] * self.NUM_LEDS

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

    def getResource(self):
        retValue = copy(self.rgbLeds)
        return retValue

    def setOneLed(self, id, color):
        if (id < 0) or (id >= self.NUM_LEDS):
            return
        with self.lock:
            self.rgbLeds[id * 3 + 0] = color[0]
            self.rgbLeds[id * 3 + 1] = color[1]
            self.rgbLeds[id * 3 + 2] = color[2]

    def save(self):
        """Сохраняем значение обновлённого массива
            функция используется после отправки
            команды устройству."""
        with self.lock:
            self.oldRgbLeds = copy(self.rgbLeds)

    def getChangeIdexes(self):
        """Возвращает список из индексов RGB светодиодов, которые
            изменились"""
        with self.lock:

            # получаем список индексов светодиодов, значения которых
            # изменились
            changedLedsIndexList = []
            for index, lastLed, newLed in izip(count(),
                                               self.oldRgbLeds,
                                               self.rgbLeds):
                if lastLed != newLed:
                    changedLedsIndexList.append(index)

            # перобаразуем в индексы RGB
            changedRgbIndexlist = [
                value // 3 for value in changedLedsIndexList]
            # убираем повторяющиеся индексы
            rgbIdList = list(set(changedRgbIndexlist))

        return rgbIdList

    def octetChanged(self, rgbIndexList):
        """Функция возвращает номер октета в
        котором изменились светодиоды, если он такой один"""

        # из rgb индексов получаем индексы изменившихся октетов
        octetIdListByRgb = [index // 8 for index in rgbIndexList]
        # убираем повторяющиеся элементы
        octetIdList = list(set(octetIdListByRgb))
        # считаем кол-во изменившихся октетов
        numChanged = len(octetIdList)
        # print("numChanged: {} | octedList: {}".format(numChanged, octetIdList))
        if numChanged == 1:
            return octetIdList[0]
        return None

    def quartetChanged(self, rgbIndexList):
        """Функция возвращает номер квартета, в котором изменились
            светодиоды, если он такой один"""

        # из rgb индексов получаем индексы изменившихся квартетов
        quartetIdListByRgb = [index // 4 for index in rgbIndexList]
        # убираем повторяющиеся элементы
        quartetIdList = list(set(quartetIdListByRgb))
        # считаем кол-во изменившихся октетов
        numChanged = len(quartetIdList)
        # print("quarte numChanged:", numChanged, " quartedList:", quartetIdList)
        if numChanged == 1:
            return quartetIdList[0]
        return None

    def oneChanged(self, rgbIndexList):
        """Функция возврщает номер светодиода, который изменился,
        если он такой один"""

        # считаем кол-во изменившихся индексов
        numChanged = len(rgbIndexList)

        if numChanged == 1:
            return rgbIndexList[0]
        return None

    def changed(self):
        return not self.equal(self.oldRgbLeds, self.rgbLeds)

    def getOctet(self, octetIndex):
        startIndex = (octetIndex * 8) * 3
        return self.rgbLeds[startIndex:startIndex + 8 * 3]

    def getQuartet(self, quartetIndex):
        startIndex = (quartetIndex * 4) * 3
        return self.rgbLeds[startIndex:startIndex + 4 * 3]

    def getRgbLed(self, rgbIndex):
        startLedIndex = rgbIndex * 3
        return self.rgbLeds[startLedIndex:startLedIndex + 3]
