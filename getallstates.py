#!/usr/bin/python
# -*- coding: utf-8 -*-

from devicecommand import DeviceCommand, CommandConst

from getbuttons import numAnswerDataBytes as buttonsAnswerDataBytes
from getbuttons import parseData as buttonsParseData

from getadc import numAnswerDataBytes as adcAnswerDataBytes
from getadc import parseData as adcParseData

from getencoders import numAnswerDataBytes as encodersAnswerDataBytes
from getencoders import parseData as encodersParseData

from getsensor import numAnswerDataBytes as sensorAnswerDataBytes
from getsensor import parseData as sensorParseData

from getstuckbuttons import numAnswerDataBytes as stuckButtonsAnswerDataBytes
from getStuckButtons import parseData as stuckButonsParseData


class getAllStates(DeviceCommand):
    """Получить значения сенсорных кнопок.
    В ответ 2а байта – попугаи сенсорной кнопки 1 и попугаи
    сенсорной кнопки 2.
    """

    # код команды
    commandCode = CommandConst.getAllStates

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
        buttonsData = data[0:buttonsAnswerDataBytes]
        # парсим функцией другого модуля, отвечающего за кнопки
        buttonsList = buttonsParseData(buttonsData)
        # buttonsList = self._parseGetButtonsData(data[0:3])
        result.append(buttonsList)

        # АЦП
        # меняем смещение входного массива на кол-во считанных элементов
        # в предыдущем блоке.
        dataIndex = dataIndex + buttonsAnswerDataBytes
        adcData = data[dataIndex:adcAnswerDataBytes]
        # парсим функцией другого модуля, отвечающего за АЦП
        adcList = adcParseData(adcData)
        # adcList = self._parseGetADCData(data[3:3 + 8])
        result.append(adcList)

        # Енкодеры
        # меняем смещение входного массива на кол-во считанных элементов
        # в предыдущем блоке.
        dataIndex = dataIndex + adcAnswerDataBytes
        encodersData = data[dataIndex:encodersAnswerDataBytes]
        # парсим функцией другого модуля, отвечающего за енкодеры
        encodersList = encodersParseData(encodersData)
        # encoderList = self._parseGetEncoderData(data[3 + 8:3 + 2 * 8])
        result.append(encodersList)

        # Сенсоры
        # меняем смещение входного массива на кол-во считанных элементов
        # в предыдущем блоке.
        dataIndex = dataIndex + encodersAnswerDataBytes
        sensorData = data[dataIndex:sensorAnswerDataBytes]
        # парсим функцией другого модуля, отвечающего за сенсоры
        sensorList = sensorParseData(sensorData)
        # sensorList = self._parseGetSensorData(data[3 + 2 * 8:3 + 2 * 8 + 2])
        result.append(sensorList)

        # "Залипшие кнопки"
        # меняем смещение входного массива на кол-во считанных элементов
        # в предыдущем блоке.
        dataIndex = dataIndex + sensorAnswerDataBytes
        stuckButtonsData = data[dataIndex:stuckButtonsAnswerDataBytes]
        # парсим функцией другого модуля, отвечающего за залипшие кнопки
        stuckButtonsList = stuckButonsParseData(stuckButtonsData)
        # stuckButtons = self._parseGetButtonsData(
        #     data[3 + 2 * 8 + 2:3 + 2 * 8 + 2 + 8])
        result.append(stuckButtonsList)

        return result

    def saveDataInSlave(self, data):
        """Если дескриптор слейва известен, то сохраняем данные,
        используя его интерфейс."""
        if self.__slave is not None:
            self.__slave.saveButtons(data[0])
            self.__slave.saveADC(data[1])
            self.__slave.saveEncoders(data[2])
            self.__slave.saveSensor(data[3])
            self.__slave.saveStuckButtons(data[4])
