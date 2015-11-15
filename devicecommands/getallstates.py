#!/usr/bin/python
# -*- coding: utf-8 -*-

from devicecommand import DeviceCommand
from commandcode import Command

from getbuttons import GetButtons

from getadc import GetADC

from getencoders import GetEncoders
# from getencoders import parseData as encodersParseData

from getsensor import GetSensor
# from getsensor import parseData as sensorParseData

from getstuckbuttons import GetStuckButtons
# from getStuckButtons import parseData as stuckButonsParseData


class GetAllStates(DeviceCommand):
    """Получить значения сенсорных кнопок.
    В ответ 2а байта – попугаи сенсорной кнопки 1 и попугаи
    сенсорной кнопки 2.
    """

    # код команды
    commandCode = Command.getAllStates

    # кол-во целых байт данных в ответе
    numAnswerDataBytes = 24

    def packagingData(self, inOutPackage, data):
        """ Упаковываем данные для отправки
        Данных для упаковки get комманд - нет"""

        return inOutPackage

    def parseData(self, data):
        """ Парсер данных всех состояний
        3и байта — состояния кнопок,
        8 байт — АЦП,
        8 байт — энкодеры,
        2а байта — сенсорные кнопки,
        3и байта — залипшие кнопки (в том порядке,
                                     как они в командах выше).

        На выходе список из 5 элементов, каждый из которых список.
        """

        if len(data) != self.numAnswerDataBytes:
            return None

        result = []
        # индекс входного массива данных
        dataIndex = 0

        # Простые кнопки
        # получаем данные из массива
        buttonsAnswerDataBytes = GetButtons.numAnswerDataBytes
        buttonsData = data[0:buttonsAnswerDataBytes]
        # парсим функцией другого модуля, отвечающего за кнопки
        buttonsList = GetButtons().parseData(buttonsData)
        print buttonsList
        result.append(buttonsList)
        dataIndex = dataIndex + buttonsAnswerDataBytes

        # АЦП
        # меняем смещение входного массива на кол-во считанных элементов
        # в предыдущем блоке.

        adcAnswerDataBytes = dataIndex + GetADC.numAnswerDataBytes
        adcData = data[dataIndex:adcAnswerDataBytes]
        # парсим функцией другого модуля, отвечающего за АЦП
        adcList = GetADC().parseData(adcData)
        result.append(adcList)
        dataIndex = adcAnswerDataBytes

        # Енкодеры
        # меняем смещение входного массива на кол-во считанных элементов
        # в предыдущем блоке.
        encodersAnswerDataBytes = dataIndex + GetEncoders.numAnswerDataBytes
        encodersData = data[dataIndex:encodersAnswerDataBytes]
        # парсим функцией другого модуля, отвечающего за енкодеры
        encodersList = GetEncoders().parseData(encodersData)
        result.append(encodersList)
        dataIndex = encodersAnswerDataBytes

        # Сенсоры
        # меняем смещение входного массива на кол-во считанных элементов
        # в предыдущем блоке.
        sensorAnswerDataBytes = dataIndex + GetSensor.numAnswerDataBytes
        sensorData = data[dataIndex:sensorAnswerDataBytes]
        # парсим функцией другого модуля, отвечающего за сенсоры
        sensorList = GetSensor().parseData(sensorData)
        result.append(sensorList)
        dataIndex = sensorAnswerDataBytes

        # "Залипшие кнопки"
        # меняем смещение входного массива на кол-во считанных элементов
        # в предыдущем блоке.
        stuckButtonsAnswerDataBytes = dataIndex + GetStuckButtons.numAnswerDataBytes
        stuckButtonsData = data[dataIndex:stuckButtonsAnswerDataBytes]
        # парсим функцией другого модуля, отвечающего за залипшие кнопки
        stuckButtonsList = GetStuckButtons().parseData(stuckButtonsData)
        result.append(stuckButtonsList)

        return result

    def saveDataInSlave(self, data):
        """Если дескриптор слейва известен, то сохраняем данные,
        используя его интерфейс."""
        if self.slave is not None:
            self.slave.saveButtons(data[0])
            self.slave.saveADC(data[1])
            self.slave.saveEncoders(data[2])
            self.slave.saveSensor(data[3])
            self.slave.saveStuckButtons(data[4])
