#!/usr/bin/python
# -*- coding: utf-8 -*-


import serial
from time import sleep

from .device import Device
from .devicecommands.commandcode import Command

import Pyro.core
import Pyro.naming
from Pyro.errors import PyroError,NamingError
import os


# Для обработки очереди команд
try:
    import Queue
except:
    import queue as Queue
import threading

# Используется при отладке.
# Данное имя используется клиентом при подключении
# Реализовано при помощи модуля Pyro
DEBUG_SERVER_NAME = "DEVICE_MASTER"
# Чтобы включить режим отладки переменная окружения
# DEBUG_GLOBAL_VARIABLE  должа быть не нулевой
DEBUG_GLOBAL_VARIABLE = "DEBUG_MASTER"
DEBUG_GLOBAL_VARIABLE_VALUE = "1"
PYRO_NS="pyro-ns &"

class DeviceMaster(Pyro.core.ObjBase):

    COM_READ_TIMEOUT = 1
    # Таймаут по записи в com-порт
    COM_WRITE_TIMEOUT = 1

    DEFAULT_BAUDRATE = 9600
    # Остальные настройки com-порта в функции _initComPort()

    def __init__(self, queueSize=10):
        # список дескрипторов устройств
        self.__slaveList = []
        # список дескрипторов com-портов
        self.__comPortList = []

        # список контекстов для потоков
        self.threadContextList = []

        # список созданных потоков
        self.threadList = []

        self.__debugMode = False

        if os.environ.get(DEBUG_GLOBAL_VARIABLE) == DEBUG_GLOBAL_VARIABLE_VALUE:
            os.system(PYRO_NS)
            self.__debugMode = True
            Pyro.core.ObjBase.__init__(self)

    def _createDebugThread(self):

        debugThread = threading.Thread(
            target=self._debugThread)

        # сохраняем дескриптор в списке
        self.threadList.append(debugThread)

        # запускаем
        debugThread.daemon = True
        debugThread.start()

    def hello(self):
        return "Hello, from deviceMaster"

    def _debugThread(self):
        Pyro.core.initServer()
        daemon = Pyro.core.Daemon()
        # locate the NS
        locator = Pyro.naming.NameServerLocator()
        print( 'searching for Name Server...')
        ns = locator.getNS()
        daemon.useNameServer(ns)

        # connect a new object implementation (first unregister previous one)
        try:
                # 'test' is the name by which our object will be known to the outside world
                ns.unregister(DEBUG_SERVER_NAME)
        except NamingError:
                pass

        # connect new object implementation
        daemon.connect(self, DEBUG_SERVER_NAME)

        # enter the server loop.
        print( 'Server object  ready.')
        daemon.requestLoop()

    def _createPortThread(self, port, slave):
        """Создаение потока работы с устройствами
        Для каждого ком-порта создаётся свой поток
        И своя очередь
        """

        # по дескриптору порта определяем существует ли для него поток
        resourse = self._getThreadContextByPort(port)

        if resourse is not None:
            # поток уже существует, добавляем в его контекст
            # дескриптор устройства
            resourse.addSlave(slave)
            return
        else:
            # создаём контекст
            threadContext = ThreadContext(port, slave)
            self.threadContextList.append(threadContext)
            # создаём поток
            portThread = threading.Thread(
                target=self._portThreadHandler,
                args=(threadContext,))

            # сохраняем дескриптор в списке
            self.threadList.append(portThread)

            # запускаем
            portThread.daemon = True
            portThread.start()

    def _initComPort(self, devComPortName):
        """Инициализация com-порта по символьному имени ser1
        или пути /dev/ser1.
        Возвращается дескриптор порта
        Исключения не обрабатываются.
        """
        # if comPort exist in list then return it
        for comPort in self.__comPortList:
            if comPort.name == devComPortName:
                return comPort

        # ComPort not exist in List ->
        #    then Open port, add in List and return
        serialDescriptor = serial.Serial(
            devComPortName, self.DEFAULT_BAUDRATE,
            timeout=self.COM_READ_TIMEOUT,
            writeTimeout=self.COM_WRITE_TIMEOUT,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE)

        self.__comPortList.append(serialDescriptor)
        return serialDescriptor

    def _getThreadContextByPort(self, port):
        for resourse in self.threadContextList:
            if port == resourse.getPort():
                return resourse

        return None

    def _portThreadHandler(self, context):
        """ Поток взаимодействия с устройством.
            Для каждого порта создаётся свой.

            Отсюда отправляются все команды.
            1) Проверяется очередь команд, которы могут быть вызваны
            из любой части программы
            2) Выполняется основная часть взаимодействия с устройствами.

            Для каждого устройства порта выполнятся опрос всех
            состояний, а потом установка новых значений, если массивы
            устройств изменились.
        """
        while True:

            # Без обращения к устройствам исчезают задержки
            # связанные с обращением к com-порту
            # чтобы не забивать процессор циклом с быстрыми
            # командами мы просто вставляем задержку.
            # чтобы исключить загрузку процессора под 100%
            if self.__debugMode:
                sleep(0.2)

            # достаём из контекста данные
            slaveList = context.getSlaves()
            port = context.getPort()
            queue = context.getQueue()

            # проверяем динамически заполняему очередь
            if not queue.empty():
                # если в очереди есть команды - выполняем одну
                slave, commad, data = queue.get()
                slave.sendCommand(commad, data)

            # выполняем запросы для каждого устройства
            for slave in slaveList:
                # команды выполняемые устройством в классе device.py
                slave.executeCommands()

    def _getSlaveDescriptor(self, slaveName):
        """Получение дескриптора устройства по имени"""
        for slave in self.__slaveList:
            if isinstance(slaveName, Device):
                if slave == slaveName:
                    return slave
            else:
                if slave.getName() == slaveName:
                    return slave
        return None

    def addSlave(self, name, comPort, address, boudrate=5):
        """
        При добалении нового устройства проверяется:
            1) инициализирован ли com-порт устройства.
            Если нет - идёт инициализация
            2) Создаётся устройство.

            3) Создаётся поток, для каждого уникального порта
                ему передаётся контекст из списка устройств с которыми
                поток должен работать.

        Параметры для добавления устройства:
        """
        # Инициализируем com-порт
        if self.__debugMode:
            comPortDescriptor = None
        else:
            comPortDescriptor = self._initComPort(comPort)

        # создаём ведомое устройство
        slave = Device(address, comPortDescriptor, name, self.__debugMode)

        self.__slaveList.append(slave)

        # меняем скорость
        slave.sendCommand(Command.changeSpeed, boudrate)
        # sleep(1)

        # # создаём поток для каждого уникального порта
        # self._createPortThread(comPortDescriptor, slave)

        return slave

    # Ещё не решил как удобнее получать ресурсы устройств.
    # Самостоятельными объектами, или просто массивами
    # Если получать просто массивами, то для записи новых значений нужно использовать функции set* мастера
    # Если получать объектами, запись в них нужно осуществлять
    # их же фунцкиями set.
    # Также в объектах храяняться их предыущие значения.
    VALUE_CLASS_OBJECT = "object"
    VALUE_CLASS_VALUE = "value"
    VALUE_CLASS_DEFAULT_VALUE = VALUE_CLASS_OBJECT


    def start(self):
        if self.__debugMode:
            self._createDebugThread()

        for slave in self.__slaveList:
            # создаём поток для каждого уникального порта
            self._createPortThread(slave.getPort(), slave)

    # АЦП
    def getAdc(self, slave, valueClass=VALUE_CLASS_DEFAULT_VALUE):
        slaveDescriptor = self._getSlaveDescriptor(slave)
        if not slaveDescriptor:
            return
        if valueClass == self.VALUE_CLASS_OBJECT:
            return slaveDescriptor.getAdc()
        return slaveDescriptor.getAdc().get()

    def setAdc(self, slave, value):
        slaveDescriptor = self._getSlaveDescriptor(slave)
        if not slaveDescriptor:
            return
        slaveDescriptor.setAdc(value)

    # Кнопки
    def getButtons(self, slave, valueClass=VALUE_CLASS_DEFAULT_VALUE):
        slaveDescriptor = self._getSlaveDescriptor(slave)
        if not slaveDescriptor:
            return
        if valueClass == self.VALUE_CLASS_OBJECT:
            return slaveDescriptor.getButtons()
        return slaveDescriptor.getButtons().get()


    def g_getButtons(self, slave, valueClass=VALUE_CLASS_DEFAULT_VALUE):
        slaveDescriptor = self._getSlaveDescriptor(slave)
        if not slaveDescriptor:
            return
        return slaveDescriptor.getButtons().get()

    def setButtons(self, slave, value):
        slaveDescriptor = self._getSlaveDescriptor(slave)
        if not slaveDescriptor:
            return
        slaveDescriptor.setButtons(value)

    # 'Залипшие' кнопки
    def getStuckButtons(self, slave, valueClass=VALUE_CLASS_DEFAULT_VALUE):
        slaveDescriptor = self._getSlaveDescriptor(slave)
        if not slaveDescriptor:
            return
        if valueClass == self.VALUE_CLASS_OBJECT:
            return slaveDescriptor.getStuckButtons()
        return slaveDescriptor.getStuckButtons().get()

    def setStuckButtons(self, slave, value):
        slaveDescriptor = self._getSlaveDescriptor(slave)
        if not slaveDescriptor:
            return
        slaveDescriptor.setStuckButtons(value)

    # Энкодеры
    def getEncoders(self, slave, valueClass=VALUE_CLASS_DEFAULT_VALUE):
        slaveDescriptor = self._getSlaveDescriptor(slave)
        if not slaveDescriptor:
            return
        if valueClass == self.VALUE_CLASS_OBJECT:
            return slaveDescriptor.getEncoders()
        return slaveDescriptor.getEncoders().get()

    def setEncoders(self, slave, value):
        slaveDescriptor = self._getSlaveDescriptor(slave)
        if not slaveDescriptor:
            return
        slaveDescriptor.setEncoders(value)

    # ЖКИ
    def getLcd(self, slave, valueClass=VALUE_CLASS_DEFAULT_VALUE):
        slaveDescriptor = self._getSlaveDescriptor(slave)
        if not slaveDescriptor:
            return
        if valueClass == self.VALUE_CLASS_OBJECT:
            return slaveDescriptor.getLcd()
        return slaveDescriptor.getLcd().get()

    def setLcd(self, slave):
        slaveDescriptor = self._getSlaveDescriptor(slave)
        if not slaveDescriptor:
            return
        slaveDescriptor.setLcd(value)

    # Реле
    def getRelays(self, slave, valueClass=VALUE_CLASS_DEFAULT_VALUE):
        slaveDescriptor = self._getSlaveDescriptor(slave)
        if not slaveDescriptor:
            return
        if valueClass == self.VALUE_CLASS_OBJECT:
            return slaveDescriptor.getRelays()
        return slaveDescriptor.getRelays().get()

    def setRelays(self, slave, value):
        slaveDescriptor = self._getSlaveDescriptor(slave)
        if not slaveDescriptor:
            return
        slaveDescriptor.setRelays(value)

    # Обычные светодиоды
    def getSimpleLeds(self, slave, valueClass=VALUE_CLASS_DEFAULT_VALUE):
        slaveDescriptor = self._getSlaveDescriptor(slave)
        if not slaveDescriptor:
            return
        if valueClass == self.VALUE_CLASS_OBJECT:
            return slaveDescriptor.getSimpleLeds()
        return slaveDescriptor.getSimpleLeds.get()

    def setSimpleLeds(self, slave, value):
        slaveDescriptor = self._getSlaveDescriptor(slave)
        if not slaveDescriptor:
            return
        slaveDescriptor.setSimpleLeds(value)

    # Умные светодиоды
    def getSmartLeds(self, slave, valueClass=VALUE_CLASS_DEFAULT_VALUE):
        slaveDescriptor = self._getSlaveDescriptor(slave)
        if not slaveDescriptor:
            return
        if valueClass == self.VALUE_CLASS_OBJECT:
            return slaveDescriptor.getSmartLeds()
        else:
            return slaveDescriptor.getSmartLeds().get()

    def setSmartLeds(self, slave, value):
        slaveDescriptor = self._getSlaveDescriptor(slave)
        if not slave:
            return
        slaveDescriptor.setSmartLeds(value)

    def getSensors(self, slave, valueClass=VALUE_CLASS_DEFAULT_VALUE):
        slaveDescriptor = self._getSlaveDescriptor(slave)
        if not slaveDescriptor:
            return
        if valueClass == self.VALUE_CLASS_OBJECT:
            return slaveDescriptor.getSensors()
        else:
            return slaveDescriptor.getSensors().get()

    def setSensors(self, slave, value):
        slaveDescriptor = self._getSlaveDescriptor(slave)
        if not slaveDescriptor:
            return
        slaveDescriptor.setSensors(value)

class ThreadContext:
    """Контекст потоков, выполняющих опрос устройств.
    Контекст создан для эффективной передачи аргументов потокам,
    с возможностью динамического добавление устройств в потоки.
    """
    DEFAULT_QUEUE_SIZE = 2

    def __init__(self, comPort, slave, qSize=2):
        self.port = comPort
        self.slaveList = [slave]
        self.queue = Queue.Queue(qSize)

    def addSlave(self, slave):
        self.slaveList.append(slave)

    def getQueue(self):
        return self.queue

    def getPort(self):
        return self.port

    def getSlaves(self):
        return self.slaveList

    def putCommand(self, slaveName, command, data=None):
        self._putCommandInQueue(slaveName, command, data)

    def _putCommandInQueue(self, slaveName, command, data=None):
        # получение дескриптора ведомого устройства
        slave = self._getSlaveDescriptor(slaveName)
        if not slave:
            # print "Not Slave", slave
            return False
        # добавление команды в очередь
        queueData = [slave, command, data]
        self.queue.put(queueData)
        return True

    def _getSlaveDescriptor(self, slaveName):
        for slave in self.slaveList:
            if isinstance(slaveName, Device):
                if slave == slaveName:
                    return slave
            else:
                if slave.getName() == slaveName:
                    return slave
        return None
