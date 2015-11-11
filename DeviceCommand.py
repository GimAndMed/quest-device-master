#!/usr/bin/python
# -*- conding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty


class DeviceCommand():
    "Абстрактный класс комманд"
    __metaclass__ = ABCMeta

    @abstractproperty
    def numAnswerBytes(): return 100

    # @abstractproperty

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
        self.getDataFromAnswer(answer)

        # возвращаем данные
        return self.getAnswerData()

    def send(self, package):
        return self.__portDescriptor.write(package)

    def receive(self):
        return self.__portDescriptor.read(self.numAnswerBytes())

    @abstractmethod
    def createPackage(): pass

    @abstractmethod
    def answerValid(self, answer): pass

    @abstractmethod
    def getDataFromAnswer(self, answer): pass


class ConnectionCheck(DeviceCommand):
    def foo(self):
        print "Foo method of ConnectionCheck"
if __name__ == '__main__':

    command = ConnectionCheck()
    command.foo()
