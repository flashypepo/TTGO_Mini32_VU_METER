"""
rtc_sync - synchronize with NTTPserver
pre-condition: device connected to Wifi
2018-0529 pepo added timerecord()
2018-0520 pepo new, extracted from ws1.py
"""
from machine import RTC
from time import sleep_ms, localtime, strftime

# real-time clock
rtc = RTC()

# test if rtc needs to be synchronized
if rtc.now()[0] < 1975:
    # get the time from NTTP-server
    rtc.ntp_sync(server='nl.pool.ntp.org', tz='CET-1CEST,M3.5.0,M10.5.0/3')
    sleep_ms(500) # small delay - trial and error

# formatted time record
def timerecord():
    return strftime("%a %d %b %Y %H:%M:%S", localtime())

# helper
def gettoday():
    return strftime("%d.%m.%Y,%H:%M:%S", localtime())


if __name__ == '__main__':
    print("It's", timerecord())

    # 2018_1201 write startup time to RTC memory
    # https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/rtc
    rtc.write_string(timerecord())
