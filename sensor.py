"""
Name: Yash Chaudhari
Date: 11/10/2025
"""
import time
from grove.adc import ADC


class Sensor:
    def __init__(self, channel=2):
        self.adc = ADC()
        self.channel = channel

    def moisture(self):
        try:
            value = self.adc.read(self.channel)
            return value
        except Exception as e:
            print("Error reading sensor:", e)
            return None