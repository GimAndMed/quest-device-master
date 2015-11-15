#!/usr/bin/python
# -*- coding: utf-8 -*-

from devicecommand import DeviceCommand
from commandcode import Command


class ConnectionCheck(DeviceCommand):

    commandCode = Command.connectionCheck

    numAnswerDataBytes = 7

    EXPECTED_DATA_HELLO = "Hello!"

    def packagingData(self, inOutPackage):
        """ Упаковываем данные для отправки
            Для комманд Get и ConnectionCheck данных для отправки нет"""
        # возвращаем тот же пакет
        return inOutPackage

    def parseData(self, data):
        """ Данные возвращаются как есть """
        return data

    def saveDataInSlave(self, data):
        pass
        # self.slave.saveConnectionCheck()

    def _answerDataValid(self, data):
        """ Проверяем, получили ли мы в ответе Hello! """

        # проверяем длину данных
        if self.numAnswerDataBytes != len(data):
            return False

        # проверяем равеноство строк
        for index, char in enumerate(data):
            if self.EXPECTED_DATA_HELLO[index] != chr(char):
                return False
        return True

    def printInfo(self):
        print "Bytes size: ", self.numAnswerBytes(), \
            " Code: ", self.commandCode


if __name__ == '__main__':
    command = ConnectionCheck(123, 12, 12)
    command.printInfo()
