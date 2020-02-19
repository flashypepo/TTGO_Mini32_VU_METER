"""
main.py - VU-meter
Source: ESP32 NeoPixel VU Meter For Audio Signals |
        MAX9814, WS2812B, and Arduino
URL: https://youtu.be/xvG_kvhBECc

History
2020-0219 add running_average, sound sensor, and neopixelchain (not used)
2020-0218 VU-meter - test neopixels
"""
# project imports
from machine import ADC, Pin
from time import sleep
import ttgo_mini32_v2 as board
# TODO: from rtc_sync import rtc, timerecord, gettoday
from neopixel import NeoPixel
# import neopixelchain
# from neopixel_animations import clear, show, bounce, cycle, rainbow_cycle

# colors
# TODO: separate module
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
BRIGHTNESS = .2


# device configuration
DIN = Pin(board.D6, Pin.OUT)  # Neopixel-stick DIN pin
NUM_PIXELS = const(8)
MICIN = Pin(board.A0)  # microphone pin

# audio levels - trial and error
NOISE = const(850)
MIN_LEVEL = NOISE
MAX_LEVEL = const(2522)


# setup sensors and actuators
def setup(mic_pin, neopixel_pin, num_neopixels):
    adc = ADC(mic_pin)  # ADC-channel for microphone on pin MICIN
    np = NeoPixel(neopixel_pin, num_neopixels)  # Neopixel stick
    return (adc, np)


# get value from ADC/microphone above noise
def value_from_microphone(adc, noise=NOISE):
    micvalue = adc.read()
    micvalue = abs(1023 - micvalue)  # remove bias of 1,25V (MAX9814) ???
    if micvalue < noise:
        micvalue = 0
    else:
        micvalue = micvalue - noise
    # TODO: filter ???
    return micvalue


# return level of mic-Pin
# 2020-0219 works best!
def level(mic, noise=NOISE):
    lvl = value_from_microphone(mic, noise)
    # print-statement for plotter (tuple!, mu-editor/Thonny)
    # print('({0:5.0f},{1:5.0f},{2:5.0f})'.format(lvl, MIN_LEVEL, MAX_LEVEL))
    return (lvl, MIN_LEVEL, MAX_LEVEL)


# 2020-0219 running-avergae according to
# Banas, Tim. "How to Calculate Running Average" sciencing.com,
# https://sciencing.com/calculate-running-average-6949441.html.
# version: 19 February 2020.
def running_average(samples=15, noise=NOISE):
    # WAIT_DELAY = 0.01  # in seconds
    total = 0
    length = 0
    minLevel = MAX_LEVEL
    maxLevel = 0
    # log_text = 'Average {0:2d} samples = {3:4.0f} ({1}/{2})'
    # log_text = log_text + '\tminLvl={4},\tmaxLvl={5}'
    for i in range(samples):
        length += 1
        # sleep(WAIT_DELAY)  # trial-and-error: must have a short delay
        data = value_from_microphone(mic, noise)
        # data = random.randint(0, 2522)
        minLevel = min(data, minLevel)
        maxLevel = max(data, maxLevel)
        total = total + data
        average = total / length
        # DEBUG: print(log_text.format(length, total, length, average, minLevel, maxLevel))
        # print-statement for plotter (tuple!, mu-editor/Thonny)
        # print('({0:5.0f},0,0)'.format(average))
        # print('(0,{0:5.0f},0)'.format(minLevel))
        # print('(0,0,{0:5.0f})'.format(maxLevel))
        # print('({0:5.0f},{1:5.0f},{1:5.0f})'.format(average, minLevel, maxLevel))
    return (average, minLevel, maxLevel)


def get_color(i, height):
    # palette = (BLACK, RED, PURPLE, GREEN, BLUE)
    if i > height:
        color = BLACK  # led off
    elif i > height - 2:  # LED color range
        color = PURPLE
    elif i > height - 4:
        color = GREEN
    elif i > height - 6:
        color = RED
    else:
        color = BLUE
    return (int(BRIGHTNESS * color[0]),
            int(BRIGHTNESS * color[1]),
            int(BRIGHTNESS * color[2]))


# ###########################
if __name__ == '__main__':
    # device configuration
    print('Device = {}'.format(board.DEVICE_ID))
    print('VU-meter ...')
    log_text = 'Average {0:2d} samples = {3:4.0f} ({1}/{2})'
    log_text = log_text + '\tminLvl={4},\tmaxLvl={5}'

    try:
        mic, np = setup(MICIN, DIN, NUM_PIXELS)
        TOP = np.n + 2  # num-pixels
        isSHOWLEVELS = True

        while True:
            sleep(0.03)  # must have a short delay
            # method 1: get height straight away
            average, minLvl, maxLvl = level(mic, NOISE)

            # method 2: get running average for N samples for height
            # height, minLvl, maxLvl = average(mic, NOISE, 10)
            # average, minLvl, maxLvl = running_average(samples=N, noise=NOISE)

            # map average to height (0.. TOP)
            height = int(TOP * (average - minLvl) / (maxLvl - minLvl))
            # print('Height = {:4.2f}'.format(height))
            # height = round(height * TOP)
            # print('Height = {:2d}'.format(height))

            if height < 0:
                height = 0
            elif height >= TOP:
                height = TOP - 3  # valid index np

            # print-statement for plotter (tuple!, mu-editor/Thonny)
            if isSHOWLEVELS is True:
                print('({},{},{})'.format(average, minLvl, maxLvl))
            else:
                print('({},0,0)'.format(height))

            # neopixels off if > height, else on
            for i in range(np.n):
                color = get_color(i, height)
                np[i] = color
            np.write()

    except KeyboardInterrupt:
        np.fill(BLACK)  # pixels off
        np.write()
        print('done')
    finally:
        # cleanup and exit main
        gc.collect()
        print('[main.py] mem_free = {} bytes'.format(gc.mem_free()))
