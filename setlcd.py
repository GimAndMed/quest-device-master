#!/usr/bin/python
# -*- coding: utf-8 -*-

from devicecommand import DeviceCommand, CommandConst


class SetLCD(DeviceCommand):
    """ Установить значения для отображения на ЖКИ
        Длина данных 80 байт.
    """

    # код команды
    commandCode = CommandConst.setLCD

    # кол-во целых байт данных в ответе
    numAnswerDataBytes = 0

    def packagingData(self, inOutPackage, data):
        """ Упаковываем данные для отправки
        Нам приходит строка на 80 символов.
        Если строка больше, то берём первые 80 символов.
        Если меньше - то дополняем до 80 пробелами"""

        LCD_STRING_lENGTH = 80
        # добавляем пустое место, если входящая строка меньше
        if len(data) < LCD_STRING_lENGTH:
            dataStr = data + (' ' * (LCD_STRING_lENGTH - len(data)))
        elif len(data) == LCD_STRING_lENGTH:
            dataStr = data
        else:
            dataStr = data[0:LCD_STRING_lENGTH]

        for charStr in dataStr:
            dataPackageBytes = self._createPackageDataBytes(ord(charStr))
            inOutPackage.extend(dataPackageBytes)

        return inOutPackage

    def parseData(self, data):
        """ В ответе данных нет: pass"""
        pass

    def saveDataInSlave(self, data):
        """ В ответе данных нет: pass"""
        pass
