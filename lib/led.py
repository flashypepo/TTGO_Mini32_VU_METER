"""
generic class LED
requires GPIO to which led is attached
2018-1227 PePo - heratbeat is _thread-savvy (Loboris up)
2018-0313 PePo new

2018-0313: move to application level
    LED_PIN: uncomment the proper connect LED
    TODO: make configuration file
    LED_PIN = const(22) # builtin LED of Lolin32 Lite
    LED_PIN = const(19) # LED, Lolin32 Lite
    LED_PIN = const(2) # LED, Adafruit Huzzah ESP8266
"""

from micropython import const
from machine import Pin
from time import ticks_ms, sleep_ms
import _thread

class Led:

    def __init__(self, pin):
        """ defines a Led-object attached to pin """
        self._pin = pin
        self._led = Pin(pin, mode=Pin.OUT,pull=Pin.PULL_UP)
        self._last = 0 # used in heartbeat

    def on(self):
        """" set led on """
        self._led.value(1)

    def off(self):
        """" set led off """
        self._led.value(0)

    def toggle(self):
        """" toggle led from on to off, or vice-versa. """
        value = self._led.value()
        if value == 1:
            value = 0
        else:
            value = 1
        self._led.value(value)

    def _heartbeat(self, isReversed=False):
        """" pulse led in heartbeat mode. Use it in a while-loop."""
        now = ticks_ms() # get millisecond counter
        # 2018-1227 add led polarity:
        #           isReversed=True - cycli off/on, else on/off
        isOn = 1 if isReversed else 0

        if now - self._last > 1000:
            self._led.value(isOn)
            self._last = now
        elif now - self._last > 900:
            self._led.value(not isOn)
        sleep_ms(10) #2018-1227: prevent watchdog jumps in

    ''' 2018-1227 DEPRECATED: not _thread- and Watchdog savvy
    def heartbeat(self):
        #self._heartbeat()
        try:
           while True:
                self._heartbeat()
        except:
            print('Heartbeat... done!')
            self.off() # led off
    '''
    # heartbeat - thread-savvy, followed thread-template
    # https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/thread
    # 2018-1227 tested okay on LolinD32 Pro, TTGO mini32
    def heartbeat(self, isReversed=False):
        _thread.allowsuspend(True)
        while True:
            ntf = _thread.getnotification()
            if ntf == _thread.EXIT:
                # return from thread terminates the thread
                #print("heartbeat: terminated")
                return
            elif ntf == _thread.SUSPEND:
                while _thread.wait() != _thread.RESUME:
                    pass
            else:
                # default notification handling
                pass

            # regular application code
            self._heartbeat(isReversed)


    ### properties
    @property
    def pin(self):
        return self._pin

    @property
    def value(self):
        return self._led.value()
