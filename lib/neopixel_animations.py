"""
collection of animation for Neopixels

pre-condition: np, neopixels already defined

2019-0808 first setup from URL-1
URL:
1. https://randomnerdtutorials.com/micropython-ws2812b-addressable-rgb-leds-neopixel-esp32-esp8266/
"""

import time

BLACK = (0, 0, 0)


# turn off all pixels
def clear(np):
    show(np, BLACK, True)


def show(np, color, refresh=True):
    np.fill(color)
    if refresh is True:
        np.write()


def bounce(np, color, wait, cycles=4):
    n = np.n
    for i in range(cycles * n):
        for j in range(n):
            np[j] = color  # 2019-0808 changed: (r, g, b)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(wait)


def cycle(np, color, wait, cycles=4):
    n = np.n
    for i in range(cycles * n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = color  # 2019-0808 changed: (r, g, b)
        np.write()
        time.sleep_ms(wait)


def wheel(pos):
    """ Input a value 0 to 255 to get a color value.
    The colours are a transition r - g - b - back to r."""
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def rainbow_cycle(np, wait, max=20):
    n = np.n
    for j in range(255):
        for i in range(n):
            rc_index = (i * 256 // n) + j
            r, g, b = wheel(rc_index & 255)
            np[i] = (int(r // max), int(g // max), int(b // max))
        np.write()
        time.sleep_ms(wait)


if __name__ == '__main__':
    from neopixel import NeoPixel
    from machine import Pin
    from time import sleep
    import ttgo_mini32_v2 as board
    num_pixels = 8
    np = NeoPixel(Pin(board.D6), num_pixels)
    color = (20, 0, 0)
    wait = 20  # in ms
    bounce(np, num_pixels, color, wait)
    sleep(1)
    show((0, 0, 0))
    cycle(np, num_pixels, color, wait)
    sleep(1)
    rainbow_cycle(np, num_pixels, wait)

    sleep(1)
    show((0, 0, 0))
