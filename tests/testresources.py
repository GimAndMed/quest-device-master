#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from ..deviceresources.relays import Relays
from ..deviceresources.adc import Adc
from ..deviceresources.buttons import Buttons
from ..deviceresources.encoders import Encoders
from ..deviceresources.lcd import Lcd
from ..deviceresources.sensors import Sensors
from ..deviceresources.simpleleds import SimpleLeds
from ..deviceresources.smartleds import SmartLeds
from ..deviceresources.stuckbuttons import StuckButtons


class ResourcesTestCase(unittest.TestCase):
    def test_get(self):
        relay = Relays()
        relayValue = relay.get()
        self.assertEqual(relayValue, [0, 0, 0, 0])
        relaySecondValue = relay.get()
        self.assertNotEqual(id(relayValue), id(relaySecondValue),
                            "Compare two objectID; must be different")

    def test_set(self):
        relay = Relays()
        valueToSet = [0, 1, 0, 1]

        relayValue = relay.get()
        self.assertNotEqual(relayValue, valueToSet)

        relay.set(valueToSet)
        self.assertEqual(relay.get(), valueToSet)

        valueToSet = [0, 1, 1, 1]
        self.assertNotEqual(relay.get(), valueToSet)


class ADCTestCase(unittest.TestCase):
    DEFAULT_VALUE = [0] * 8
    NEW_VALUE = [252, 2, 14, 12, 0, 14, 12 ,2]
    CHANGED_NEW_VALUE = [0, 2, 14, 12, 0, 14, 0, 15]

    def test_get(self):
        adc = Adc()
        adcValue = adc.get()
        self.assertEqual(adcValue, self.DEFAULT_VALUE)
        adcSecondValue = adc.get()
        self.assertNotEqual(id(adcValue), id(adcSecondValue),
                            "Compare two objectID; must be different")

    def test_set(self):
        adc = Adc()
        valueToSet = self.NEW_VALUE

        adcValue = adc.get()
        self.assertNotEqual(adcValue, valueToSet)

        adc.set(valueToSet)
        self.assertEqual(adc.get(), valueToSet)

        valueToSet = self.CHANGED_NEW_VALUE
        self.assertNotEqual(adc.get(), valueToSet)

class ButtonsTestCase(unittest.TestCase):
    DEFAULT_VALUE = [0] * 18
    NEW_VALUE = [1, 0, 0, 1, 0, 0, 0, 1, 1] * 2
    CHANGED_NEW_VALUE = [1, 1, 1, 1, 1, 0, 0, 1, 1] * 2

    def test_get(self):
        buttons = Buttons()
        buttonsValue = buttons.get()
        self.assertEqual(buttonsValue, self.DEFAULT_VALUE)
        buttonsSecondValue = buttons.get()
        self.assertNotEqual(id(buttonsValue), id(buttonsSecondValue),
                            "Compare two objectID; must be different")

    def test_set(self):
        buttons = Buttons()
        valueToSet = self.NEW_VALUE

        buttonsValue = buttons.get()
        self.assertNotEqual(buttonsValue, valueToSet)

        buttons.set(valueToSet)
        self.assertEqual(buttons.get(), valueToSet)

        valueToSet = self.CHANGED_NEW_VALUE
        self.assertNotEqual(buttons.get(), valueToSet)

class EncodersTestCase(unittest.TestCase):
    DEFAULT_VALUE = [0] * 8
    NEW_VALUE = [24, 12, 100, 15, 22, 81, 56, 200]
    CHANGED_NEW_VALUE = [0, 12, 0, 15, 0, 81, 56, 200]

    def test_get(self):
        encoders = Encoders()
        encodersValue = encoders.get()
        self.assertEqual(encodersValue, self.DEFAULT_VALUE)
        encodersSecondValue = encoders.get()
        self.assertNotEqual(id(encodersValue), id(encodersSecondValue),
                            "Compare two objectID; must be different")

    def test_set(self):
        encoders = Encoders()
        valueToSet = self.NEW_VALUE

        encodersValue = encoders.get()
        self.assertNotEqual(encodersValue, valueToSet)

        encoders.set(valueToSet)
        self.assertEqual(encoders.get(), valueToSet)

        valueToSet = self.CHANGED_NEW_VALUE
        self.assertNotEqual(encoders.get(), valueToSet)

class LcdTestCase(unittest.TestCase):
    DEFAULT_VALUE = [0] * 80
    NEW_VALUE = "Hello, Man"
    CHANGED_NEW_VALUE = "What's up!"

    def test_get(self):
        lcd = Lcd()
        lcdValue = lcd.get()
        self.assertEqual(lcdValue, self.DEFAULT_VALUE)
        lcdSecondValue = lcd.get()
        self.assertNotEqual(id(lcdValue), id(lcdSecondValue),
                            "Compare two objectID; must be different")

    def test_set(self):
        lcd = Lcd()
        valueToSet = self.NEW_VALUE + ' '*(len(self.DEFAULT_VALUE) - len(self.NEW_VALUE))

        lcdValue = lcd.get()
        self.assertNotEqual(lcdValue, valueToSet)

        lcd.set(valueToSet)
        self.assertEqual(lcd.get(), valueToSet)

        valueToSet = self.CHANGED_NEW_VALUE + ' '*(len(self.DEFAULT_VALUE) - len(self.CHANGED_NEW_VALUE))
        self.assertNotEqual(lcd.get(), valueToSet)


class SensorsTestCase(unittest.TestCase):
    DEFAULT_VALUE = [0] * 2
    NEW_VALUE = [220, 100]
    CHANGED_NEW_VALUE = [110, 0]

    def test_get(self):
        sensors = Sensors()
        sensorsValue = sensors.get()
        self.assertEqual(sensorsValue, self.DEFAULT_VALUE)
        sensorsSecondValue = sensors.get()
        self.assertNotEqual(id(sensorsValue), id(sensorsSecondValue),
                            "Compare two objectID; must be different")

    def test_set(self):
        sensors = Sensors()
        valueToSet = self.NEW_VALUE

        sensorsValue = sensors.get()
        self.assertNotEqual(sensorsValue, valueToSet)

        sensors.set(valueToSet)
        self.assertEqual(sensors.get(), valueToSet)

        valueToSet = self.CHANGED_NEW_VALUE
        self.assertNotEqual(sensors.get(), valueToSet)

class SimpleLedsTestCase(unittest.TestCase):
    DEFAULT_VALUE = [0] * 80
    NEW_VALUE = [1, 1, 0, 1] * 20
    CHANGED_NEW_VALUE = [0, 1, 1, 0] * 20

    def test_get(self):
        simpleLeds = SimpleLeds()
        simpleLedsValue = simpleLeds.get()
        self.assertEqual(simpleLedsValue, self.DEFAULT_VALUE)
        simpleLedsSecondValue = simpleLeds.get()
        self.assertNotEqual(id(simpleLedsValue), id(simpleLedsSecondValue),
                            "Compare two objectID; must be different")

    def test_set(self):
        simpleLeds = SimpleLeds()
        valueToSet = self.NEW_VALUE

        simpleLedsValue = simpleLeds.get()

        self.assertNotEqual(simpleLedsValue, valueToSet)

        simpleLeds.set(valueToSet)
        self.assertEqual(simpleLeds.get(), valueToSet)

        valueToSet = self.CHANGED_NEW_VALUE
        self.assertNotEqual(simpleLeds.get(), valueToSet)

class SmartLedsTestCase(unittest.TestCase):
    DEFAULT_VALUE = [0, 0, 0] * 32
    NEW_VALUE = [0xff, 0xAA, 0xAA] * 32
    CHANGED_NEW_VALUE = [0, 1, 1, 0] * 32

    def test_get(self):
        smartLeds = SmartLeds()
        smartLedsValue = smartLeds.get()
        self.assertEqual(smartLedsValue, self.DEFAULT_VALUE)
        smartLedsSecondValue = smartLeds.get()
        self.assertNotEqual(id(smartLedsValue), id(smartLedsSecondValue),
                            "Compare two objectID; must be different")

    def test_set(self):
        smartLeds = SmartLeds()
        valueToSet = self.NEW_VALUE

        smartLedsValue = smartLeds.get()

        self.assertNotEqual(smartLedsValue, valueToSet)

        smartLeds.set(valueToSet)
        self.assertEqual(smartLeds.get(), valueToSet)

        valueToSet = self.CHANGED_NEW_VALUE
        self.assertNotEqual(smartLeds.get(), valueToSet)

class StuckButtonsTestCase(unittest.TestCase):
    DEFAULT_VALUE = [0] * 18
    NEW_VALUE = [1, 0, 1, 1, 1, 1, 1, 0, 0] * 2
    CHANGED_NEW_VALUE = [1, 0, 1, 1, 0, 0, 0, 0, 1] * 2

    def test_get(self):
        stuckButtons = StuckButtons()
        stuckButtonsValue = stuckButtons.get()
        self.assertEqual(stuckButtonsValue, self.DEFAULT_VALUE)
        stuckButtonsSecondValue = stuckButtons.get()
        self.assertNotEqual(id(stuckButtonsValue), id(stuckButtonsSecondValue),
                            "Compare two objectID; must be different")

    def test_set(self):
        stuckButtons = StuckButtons()
        valueToSet = self.NEW_VALUE

        stuckButtonsValue = stuckButtons.get()

        self.assertNotEqual(stuckButtonsValue, valueToSet)

        stuckButtons.set(valueToSet)
        self.assertEqual(stuckButtons.get(), valueToSet)

        valueToSet = self.CHANGED_NEW_VALUE
        self.assertNotEqual(stuckButtons.get(), valueToSet)



if __name__ == "__main__":
    # relay = Relays()
    # print relay.get()
    # relay.set([1,1,0,1])
    pass
