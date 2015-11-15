#!/usr/bin/python
# -*- coding: utf-8 -*-

from devicecommand import DeviceCommand, CommandConst


class GetStuckButtons(DeviceCommand):
    """Получить значения "залипших" кнопок.
        Кнопок, чьё состояние сохраняется при нажатии и сбрасывается,
            только при считывании.
        Команда для кнопок, чьё состояние можно не успеть считать
            вовремя.
        В ответ 3 байта, используемые биты 0 – 17. Бит 0 всегда 0.
    """

    # код команды
    commandCode = CommandConst.getStuckButtons

    # кол-во целых байт данных в ответе
    numAnswerDataBytes = 3

    def packagingData(self, inOutPackage, data):
        """ Упаковываем данные для отправки
        Данных для упаковки get комманд - нет"""

        return inOutPackage

    def parseData(self, data):
        """ В ответе 3 байта:  используемые биты 0 - 17"""
        if len(data) != 3:
            # logPackage.debug("For command getButtons data length\
            #  must be 3 bytes but we have: %d", len(data))
            return None
        buttonsList = []
        for dataByte in data:
            for i in range(0, 8):
                button = (dataByte >> i) & 0x01
                buttonsList.append(button)
        return buttonsList

    def saveDataInSlave(self, data):
        """Если дескриптор слейва известен, то сохраняем данные,
        используя его интерфейс."""
        if self.__slave is not None:
            self.__slave.saveStuckButtons(data)
