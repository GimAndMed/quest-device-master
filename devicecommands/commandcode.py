#!/usr/bin/python
# -*- coding: utf-8 -*-


class Command:
    """Коды команд согласно протоколу"""
    connectionCheck = 0x00
    changeSpeed = 0x01

    setSimpleLeds = 0x10
    setSmartLeds = 0x11
    setSmartOctetLeds = 0x14
    setSmartQuartetLeds = 0x15
    setSmartOneLeds = 0x16
    setLCD = 0x12
    setRelays = 0x13

    getButtons = 0x20
    getADC = 0x21
    getEncoders = 0x22
    getSensor = 0x23
    getStuckButtons = 0x24
    getAllStates = 0x2F
    unknown = 0x56


def commandTypeIsSet(commandCode):
    """Проверка, что команда я вляется командой установки значений"""
    if (commandCode >> 4) & 0x0f <= 1:
        return True
    return False


def commandTypeIsGet(commandCode):
    """Проверка, что команда я вляется командой получения значений"""
    if (commandCode >> 4) & 0x0f == 2:
        return True
    return False
