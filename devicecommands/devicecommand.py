#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty
from .commandcode import Command, commandTypeIsGet, commandTypeIsSet
import logging
from serial import SerialTimeoutException
# для отладочного вывода
logging.basicConfig(
    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s%(message)s',
    level=logging.DEBUG)
commandLogger = logging.getLogger('package')
logging.disable(logging.DEBUG)
import time
# logging.disable(logging.NOTSET)


class DeviceCommand():
    "Абстрактный класс комманд"
    __metaclass__ = ABCMeta

    # константы
    # Кол-во байт занимаемых стартовым байтом, байтом команды и CRC
    START_COMMAND_CRC_SIZE = 5
    # Одни байт данных в пакете занимает 2 (старший и младший)
    DATA_BYTE_SIZE = 2

    def __init__(self, port=None, address=None, data=None, slave=None):
        self.init(port, address, data, slave)

    def init(self, port, address, data=None, slave=None):
        self.portDescriptor = port
        self.address = address
        self.data = data
        # объект к которому выполняется запрос
        self.slave = slave
        self.connection = False

    @abstractproperty
    def numAnswerDataBytes(self):
        """ Кол-во байтов данных в пакете (не старших и младших) """
        return 93

    @abstractproperty
    def commandCode(self):
        """ Код команды, или тип, содержится в классе Command """
        return Command.unknown

    def numAnswerBytes(self):
        number = self.START_COMMAND_CRC_SIZE + \
            self.DATA_BYTE_SIZE * self.numAnswerDataBytes
        return number

    @abstractmethod
    def packagingData(self, inOutPackage, data): pass

    @abstractmethod
    def parseData(self, data): pass

    @abstractmethod
    def saveDataInSlave(self, data): pass

    # @abstractmethod
    # def getSlaveData(self): pass

    def execute(self):
        """Выполнение запроса к устройству
        с ожиданием ответа
        Выполняется создание соответствующего команде
        пакета. Его отправка и приём от устройства результата."""

        commandLogger.debug("Command << {command} >> ".format(
            command=self.__class__.__name__))

        # создаём пакет
        package = self.createPackage(self.data)
        # печатаем
        self._printPackage(package, "{} Send:".format(self.__class__.__name__))

        # отправляем его в порт
        # try:
        self.send(package)
        # except SerialTimeoutException:
        #     return False

        # получаем ответ
        answer = self.receive()
        # печатаем
        self._printPackage(
            answer, "{} Receive:".format(self.__class__.__name__))

        # определяем что ответ валидный
        # слейв понял нашу команду и выполнил
        if (not self.answerValid(answer)):
            
            self.portDescriptor.flush()
            self.portDescriptor.close()
            time.sleep(1)
            self.portDescriptor.open()
            time.sleep(1)
            return False

        # берём из ответного пакета данные
        data = self.getDataFromAnswer(answer)

        formattedData = self.parseData(data)

        # сохраняем данные с помощью функций слейва.
        self.saveDataInSlave(formattedData)

        if formattedData is None:
            returnValue = True
        else:
            returnValue = formattedData

        logging.debug("return: \n\t{}".format(returnValue))

        return returnValue

    def send(self, package):
        # return self.portDescriptor.write(str(bytearray(package)))
        return self.portDescriptor.write(package)

    def receive(self):
        return self.portDescriptor.read(self.numAnswerBytes())

    def answerValid(self, answer):
        """ Определение валидности ответного пакета """
        # длина должна быть больше или равна минимальному возм. размеру

        if len(answer) < self.START_COMMAND_CRC_SIZE:
            logging.info('[AnswerValid: answer length error] Command:'
                         ' {command} | expect >= {expectLen} |'
                         ' actualy: {actualyLen}'.format(
                             command=self.__class__.__name__,
                             expectLen=self.START_COMMAND_CRC_SIZE,
                             actualyLen=len(answer)
                         ))
            return False

        # получателем должен быть мастер 0x80
        startByte = answer[0]
        if isinstance(answer[0], int):
            startByte = answer[0]
        else:
            startByte = ord(answer[0])

        if 0x80 != startByte:
            commandLogger.info("{command}: [Error] Answer startByte not for us! 0x80 = {startB}".format(
                command=self.__class__.__name__, startB=startByte))
            return False

        # считаем сrc и сравниваем с тем, что получили
        receiveCrc = self._getDataFromBytes(
            answer[-2], answer[-1])
        countCrcValue = self._countPackageCRC(answer[:-2])

        if (receiveCrc != countCrcValue):
            commandLogger.info("{command}: [Error] CRC answer! Expect: {expectCRC} Receive: {recCRC}".format(
                command=self.__class__.__name__, expectCRC=countCrcValue, recCRC=receiveCrc))
            return False

        # Если слейв понял команду установки значений, то он возвращает
        # в коде команды 0x80
        # Если не понял, то в поле команды выставляется 0x81
        # Если команда получения значения, то в ответе дублируется.
        receiveCommand = self._getDataFromBytes(answer[1], answer[2])

        if receiveCommand == 0x81:
            commandLogger.info("{command}: [Error] Slave return message: Unknown command".format(
                command=self.__class__.__name__))
            return False

        if commandTypeIsGet(self.commandCode) and \
                self.commandCode == receiveCommand:
            pass

        elif commandTypeIsSet(self.commandCode) and \
                receiveCommand == 0x80:
            pass
        else:
            commandLogger.info("{command}: [Error] Slave receive unknown command code".format(
                self.__class__.__name__))
            return False

        # валидное ли кол-во данных у пакета
        if self._answerDataValid(answer[3:-2]):
            return True

        commandLogger.info(
            "{command}: [Error] Length data not valid".format(self.__class__.__name__))
        return False

    def _answerDataValid(self, answerData):
        """ Определяем правльное ли число байт мы ожидали """
        if 0 == len(answerData):
            answerLen = 0
        else:
            answerLen = len(answerData) / 2

        if answerLen == self.numAnswerDataBytes:
            return True
        return False

    def createPackage(self, data):
        package = []

        startByte = self._createPackageByte(self.PackageIndicator.new,
                                            None, None,
                                            self.address, None)
        package.append(startByte)

        # создаём байты команды
        commandPackageBytes = self._createCommandBytes(self.commandCode)
        package.extend(commandPackageBytes)

        # упаковываем данные
        package = self.packagingData(package, data)

        # считаем и упаковывае crc
        crcPackageBytes = self._createCRCPackageBytes(package)
        package.extend(crcPackageBytes)

        return package

    class PackageIndicator:
        new, old = range(2)

    class TetradeType:
        shift = 6  # сдвиг влево
        hight = 0x01 << shift
        low = 0x00 << shift

    class ByteType:
        shift = 4
        command = 0x00 << shift
        data = 0x01 << shift
        crc = 0x02 << shift
        reserved = 0x03 << shift

    def _createCommandBytes(self, command):
        """ Функция создания байтов команды для пакета """

        # создание байтов команды
        # получаем старшую тетраду кода команды
        commandCodeH = command >> 4
        # - старший байт
        commandByteH = self._createPackageByte(
            None, self.ByteType.command,
            self.TetradeType.hight, None,
            commandCodeH)

        # - младший байт
        commandCodeL = command & 0x0f
        commandByteL = self._createPackageByte(
            None, self.ByteType.command,
            self.TetradeType.low, None,
            commandCodeL)
        return [commandByteH, commandByteL]

    def _createPackageByte(self, packageIndicator, byteType,
                           tetradeType, address, data):
        # создаём стартовый байт
        if (self.PackageIndicator.new == packageIndicator):
            # установиливаем 7 бит: признак начала новой посылки
            packageByteStart = 0b10000000
            # добавляем адрес в поле данных
            packageByteStart |= address
            # print 'Start package byte: ', bin(packageByteStart)
            return packageByteStart
        # создание байтов остальных типов
        # - обнулим старшую тетраду на всякий случай
        data &= 0b00001111
        packageByte = 0x00
        packageByte |= byteType | tetradeType | data
        return packageByte

    def _createPackageDataBytes(self, dataByte):
        """ Функция преобразующая байт данных в два пакетных байта """
        # print "Data Byte = ", dataByte
        # разделяем на старшую и младшую тетрады
        dataValueH = dataByte >> 4
        dataValueL = dataByte & 0x0f

        dataByteH = self._createPackageByte(None, self.ByteType.data,
                                            self.TetradeType.hight,
                                            None, dataValueH)
        dataByteL = self._createPackageByte(None, self.ByteType.data,
                                            self.TetradeType.low,
                                            None, dataValueL)
        return [dataByteH, dataByteL]

    def _createCRCPackageBytes(self, package):
        """Функция формирования байтов контрольной суммы для пакета"""
        crcByte = self._countPackageCRC(package)
        crcValueH = crcByte >> 4
        crcValueL = crcByte & 0x0f
        crcByteH = self._createPackageByte(None, self.ByteType.crc,
                                           self.TetradeType.hight,
                                           None, crcValueH)
        crcByteL = self._createPackageByte(None, self.ByteType.crc,
                                           self.TetradeType.low,
                                           None, crcValueL)
        return [crcByteH, crcByteL]

    def _countPackageCRC(self, package):
        """Подсчтёт контрольной суммы:
            контрольная сумма - это младший байт суммы
            всех байтов пакета кроме самой контрольной суммы
        """
        crc = 0
        for packageByte in package:
            # Отправляем мы массив байт, а получаем массив str
            # так что надо проверить, и если необходимо преобразовать в int
            if isinstance(packageByte, int):
                intByte = packageByte
            else:
                intByte = ord(packageByte)
            crc += intByte
        crcL = crc & 0xff
        # logPackage.debug("CRC: %s Lbyte: %s",
        #                  "{0}(0b{0:08b})".format(crc), bin(crcL))
        return crcL

    def _getDataFromBytes(self, hightByteIN, lowByteIN):
        """ Функция получения байта данных из двух пакетных байтов"""
        if isinstance(hightByteIN, int):
            hightByte = hightByteIN
        else:
            hightByte = ord(hightByteIN)

        hightData = (hightByte & 0x0f) << 4

        if lowByteIN is None:
            lowData = 0x00
        else:
            if isinstance(lowByteIN, int):
                lowByte = lowByteIN
            else:
                lowByte = ord(lowByteIN)
            lowData = (lowByte & 0x0f)

        return hightData | lowData

    def getDataFromAnswer(self, answer):
        """ Получение чистых данных пакета. на выходе список """
        # исключаем стартовый байт, байты комманды, crc
        packageData = answer[3:-2]

        realData = []
        for i in range(0, len(packageData), 2):
            if len(packageData) - 1 != i:
                realDataByte = self._getDataFromBytes(
                    packageData[i], packageData[i + 1])
            else:
                realDataByte = self._getDataFromBytes(
                    packageData[i], None)
            realData.extend([realDataByte])

        return realData

    def _printBytes(self, array, receiveSend=''):
        if array is None:
            return
        for index, byte in enumerate(array):
            if not isinstance(byte, list):
                byteList = [byte]
            else:
                byteList = byte
            for listIndex, byteR in enumerate(byteList):
                # Отправляем мы массив байт, а получаем массив str
                # так что надо проверить, и если необходимо преобразовать в int
                if isinstance(byteR, int):
                    binHexStr = 'int: {0:>5d} hex: 0x{0:>02x}' \
                        '   bin: 0b{0:>08b}'.format(byteR)
                else:
                    binHexStr = 'int: {0:>5d} hex: 0x{0:>02x}' \
                        '   bin: 0b{0:>08b}'.format(ord(byteR))
                # print(" %s [%2d] %s", receiveSend, index + listIndex,
                #      binHexStr)
                commandLogger.debug(" %s [%2d] %s",
                                    receiveSend,
                                    index + listIndex,
                                    binHexStr)

    def _printPackage(self, array, receiveSend):

        if array is None:
            return

        numPackageBytes = 0
        for index, byte in enumerate(array):
            if not isinstance(byte, list):
                byteList = [byte]
            else:
                byteList = byte
            numPackageBytes = numPackageBytes + len(byteList)

        for index, byte in enumerate(array):
            if not isinstance(byte, list):
                byteList = [byte]
            else:
                byteList = byte
            for listIndex, byteR in enumerate(byteList):
                # Отправляем мы массив байт, а получаем массив str
                # так что надо проверить, и если необходимо преобразовать в int
                if isinstance(byteR, int):
                    binHexStr = 'int: {0:>5d} hex: 0x{0:>02x}' \
                        '   bin: 0b{0:>08b}'.format(byteR)
                else:
                    binHexStr = 'int: {0:>5d} hex: 0x{0:>02x}' \
                        '   bin: 0b{0:>08b}'.format(ord(byteR))
                # print(" %s [%2d] %s", receiveSend, index + listIndex,
                #      binHexStr)
                packageIndex = index + listIndex
                dataByteCounter = packageIndex / 2

                if packageIndex == 0:
                    byteType = "startB"
                elif 0 < packageIndex < 3:
                    byteType = "CmdB"
                elif 2 < packageIndex < numPackageBytes - 2:
                    byteType = "dataB"
                else:
                    byteType = "crc"

                if packageIndex % 2 == 0:
                    byteType = byteType + "_L"
                    byteNumber = ""
                else:
                    byteType = byteType + "_H"
                    if 2 < packageIndex < numPackageBytes - 2:
                        byteNumber = str(dataByteCounter)
                    else:
                        byteNumber = ""
                # commandLogger.debug(" %s %8s [%2d, %2s] %s",
                # receiveSend,
                #                    byteType,
                #                    packageIndex,
                #                    byteNumber,
                #                    binHexStr)
                printStr = "{message} {byteType:8} [{dataNumber:2}, {byteNumber:2}] {binHexStr}"
                commandLogger.debug(printStr.format(message=receiveSend,
                                                    byteType=byteType,
                                                    byteNumber=packageIndex,
                                                    dataNumber=byteNumber,
                                                    binHexStr=binHexStr))
