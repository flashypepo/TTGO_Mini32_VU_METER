"""
ttgo_mini32_v2 - pin layout specifications
added D1 mini pins for compatbility

2019-0808 - v0.1 - Initial implementation
__repro__: https://github.com/LilyGO/ESP32-MINI-32-V2.0

"""

# Import required libraries
from micropython import const
from machine import Pin, SPI, ADC
import machine
import time
import esp32

DEVICE_ID = b'TTGO mini32 v2'

# builtin LED
BUILTIN_LED = const(22)  # reversed LED!

# Hardware Pin Assingments
# TODO: I2C mapping D1 mini

# I2C
I2C_SDA = const(21)
I2C_SCL = const(22)

# SPI
SPI_MOSI = const(23)
SPI_CLK = const(18)
SPI_MISO = const(19)
SPI_SS = const(5)

# DAC
DAC1 = const(25)
DAC2 = const(26)

# ADC
ADC1_0 = const(36)
ADC1_3 = const(39)
ADC1_4 = const(32)
ADC1_5 = const(33)
ADC1_6 = const(34)
ADC1_7 = const(35)

ADC2_0 = const(4)
ADC2_2 = const(2)
ADC2_3 = const(15)
ADC2_4 = const(13)
ADC2_5 = const(12)
ADC2_6 = const(14)
ADC2_7 = const(17)
ADC2_8 = const(25)
ADC2_9 = const(26)

# D1 mini compatbility
# D1 mini mapping to GPIO pins
# __repro__ http://www.esp32learning.com/micropython/esp32-and-ws2812b-led-micropython-examples.php
D1 = const(22)
D2 = const(21)
D3 = const(17)
D4 = const(16)

A0 = const(36)
D0 = const(26)
D5 = const(18)
D6 = const(19)
D7 = const(23)
D8 = const(5)


# Touch
TOUCH0 = const(4)
TOUCH1 = const(13)
TOUCH2 = const(2)
TOUCH3 = const(15)
TOUCH5 = const(12)
TOUCH6 = const(14)
TOUCH7 = const(17)
TOUCH8 = const(33)
TOUCH9 = const(32)


# Helper functions

def get_internal_temp_F():
    """Return the internal ESP32 temperature in farenheit."""
    return esp32.raw_temperature()


def get_internal_temp_C():
    """Return the internal ESP32 temperature in celcius."""
    return (esp32.raw_temperature()-32)/1.8
