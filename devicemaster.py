#!/usr/bin/python
# -*- coding: utf-8 -*-


import serial
from time import sleep

from device import Device
from devicecommands.commandcode import Command


# Для обработки очереди команд
import Queue
import threading


class DeviceMaster:

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
                # self.sendGetAllStates(slave)
                # посылка команд установки значений
                # (посылаются в зависимости от того, изменилось ли
                #   что-нибудь с прошлого опроса)
                # self._sendSetAll(slave)

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
        comPortDescriptor = self._initComPort(comPort)

        # создаём ведомое устройство
        slave = Device(address, comPortDescriptor, name)

        self.__slaveList.append(slave)

        # меняем скорость
        slave.sendCommand(Command.changeSpeed, boudrate)
        sleep(1)

        # создаём поток для каждого уникального порта
        self._createPortThread(comPortDescriptor, slave)

        return slave

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
                args=(threadContext))
            portThread.daemon = True
            portThread.start()

    def _getThreadContextByPort(self, port):
        for resourse in self.threadContextList:
            if port == resourse.getPort():
                return resourse

        return None

    def sendGetAllStates(self, slave):
        slaveDescriptor = self._getSlaveDescriptor(slave)
        slaveDescriptor.sendCommand(Command.getAllStates)


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
