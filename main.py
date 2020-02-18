"""
main.py - VU-meter
Source: ESP32 NeoPixel VU Meter For Audio Signals |
        MAX9814, WS2812B, and Arduino
URL: https://youtu.be/xvG_kvhBECc

History
2020-0218 VU-meter - test neopixels
"""
# project imports
from machine import Pin
from time import sleep
import ttgo_mini32_v2 as board
# TODO: from rtc_sync import rtc, timerecord, gettoday
from neopixel import NeoPixel
from neopixel_animations import clear, show, bounce, cycle, rainbow_cycle

# device configuration
DIN = Pin(board.D6, Pin.OUT)  # Neopixel-stick DIN pin
NUM_PIXELS = const(16)
MICIN = Pin(board.A0)  # microphone pin


def test_audio():
    print('TODO clap detection...')


def test_neopixels():
    print('Testing {} neopixels...'.format(NUM_PIXELS))
    np = NeoPixel(DIN, NUM_PIXELS)
    color = (0, 20, 0)  # test: Green
    wait = 20  # in ms
    try:
        while True:
            print('bounce...')
            bounce(np, color, wait, 12)
            sleep(1)
            color = (0, 0, 20)  # test: Blue
            print('cycle...')
            cycle(np, color, wait, 50)
            sleep(1)
            print('rainbow...')
            rainbow_cycle(np, 50, 20)  # 2020-0218 PP added max_intensity
            sleep(1)
            # show(np, (0, 0, 0))  # off
            clear(np)
            print('waiting for next cycle...')
            sleep(20)
    except KeyboardInterrupt:
        clear(np)  # pixels off
        pass
    finally:
        print('Test neopixels done.')


# ###########################
if __name__ == '__main__':
    # device configuration
    print('Device = {}'.format(board.DEVICE_ID))
    print('VU-meter ...')
    test_audio()
    test_neopixels()
    # cleanup and exit main
    gc.collect()
    print('[main.py] mem_free = {} bytes'.format(gc.mem_free()))
