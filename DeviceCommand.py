#!/usr/bin/python
# -*- conding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty


class CommandConst:
    """ Коды всех команд """
    connectionCheck = 0x00
    changeSpeed = 0x01

    setSimpleLEDs = 0x10
    setSmartLEDs = 0x11
    setSmartOctetLEDs = 0x14
    setSmartQuartetLEDs = 0x15
    setSmartOneLEDs = 0x16
    setLCD = 0x12
    setRelays = 0x13

    getButtons = 0x20
    getADC = 0x21
    getEncoder = 0x22
    getSensor = 0x23
    getStuckButtons = 0x24
    getAllState = 0x2F
    unknown = 0x56


class DeviceCommand():
    "Абстрактный класс комманд"
    __metaclass__ = ABCMeta

    # константы
    # Кол-во байт занимаемых стартовым байтом, байтом команды и CRC
    START_COMMAND_CRC_SIZE = 5
    # Одни байт данных в пакете занимает 2 (старший и младший)
    DATA_BYTE_SIZE = 2

    @abstractproperty
    def numAnswerDataBytes(self):
        """ Кол-во байтов данных в пакете (не старших и младших) """
        return 93

    @abstractproperty
    def commandCode(self):
        """ Код команды, или тип, содержится в классе CommandConst """
        return CommandConst.unknown

    def numAnswerBytes(self):
        number = self.START_COMMAND_CRC_SIZE + self.DATA_BYTE_SIZE
        + self.numAnswerDataBytes()
        return number

    def __init__(self, port, address, slave):
        self.__portDescriptor = port
        self.__address = address
        # self.__data = None
        # объект к которому выполняется запрос
        self.__slave = None
        self.__connection = False

    # @abstractmthod
    def execute(self):
        """Выполнение запроса к устройству
        с ожиданием ответа
        Выполняется создание соответствующего команде
        пакета. Его отправка и приём от устройства результата."""
        pass

        # создаём пакет
        package = self.createPackage()

        # отправляем его в порт
        self.send(package)

        # получаем ответ
        answer = self.receive()

        # определяем что ответ валидный
        # слейв понял нашу команду и выполнил
        self.answerValid(answer)

        # берём из ответного пакета данные
        data = self.getDataFromAnswer(answer)

        # сохраняем данные с помощью функций слейва.
        self.saveDataInSlave(data)

    def send(self, package):
        return self.__portDescriptor.write(package)

    def receive(self):
        return self.__portDescriptor.read(self.numAnswerBytes())

    @abstractmethod
    def answerValid(self, answer): pass

    @abstractmethod
    def getDataFromAnswer(self, answer): pass

    @abstractmethod
    def saveDataInSlave(self, data): pass

    @abstractmethod
    def packagingData(self): pass

    @abstractmethod
    def getSlaveData(self): pass

    def createPackage(self):
        package = []

        startByte = self._createPackageByte(self.PackageIndicator.new,
                                            None, None,
                                            self.__address, None)
        package.append(startByte)

        # создаём байты команды
        commandPackageBytes = self._createCommandBytes(self.commandCode)
        package.extend(commandPackageBytes)

        # упаковываем данные
        package = self.packagingData(package)

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
