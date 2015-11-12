#!/usr/bin/python
# -*- conding: utf-8 -*-

from DeviceCommand import DeviceCommand, CommandConst


class ConnectionCheck(DeviceCommand):

    commandCode = CommandConst.connectionCheck

    numAnswerDataBytes = 7

    def packagingData(self): pass

    def answerValid(self, answer): pass

    def getDataFromAnswer(self, answer): pass

    def saveDataInSlave(self, data): pass

    def printBytesNum(self):
        print "Bytes size: ", self.numAnswerBytes()


# if __name__ = '__main__'
