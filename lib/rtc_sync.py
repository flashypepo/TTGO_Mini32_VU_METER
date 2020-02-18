"""
rtc_sync - synchronize with NTTPserver
pre-condition: device connected to Wifi

TODO: make use of RTC-shield for TinyPICO,
      especially when no internet connection

2019-0217 micropython.org version
2018-0529 pepo added timerecord()
2018-0520 pepo new, extracted from ws1.py
"""
from machine import RTC
import time

from ntptime import settime
try:
    # 2019-0803: get time from NTTP server and update RTC
    settime()
except IndexError as ex:
    print('settime() IndexError: {}'.format(ex))
    print('\t-> probably no internet connection')
    pass
except OSError as ex:
    print('boot.py: settime() OSError: {}'.format(ex))
    pass

# real-time clock
rtc = RTC()

'''lobo: test if rtc needs to be synchronized
if rtc.now()[0] < 1975:
    #get the time from NTTP-server
    rtc.ntp_sync(server='nl.pool.ntp.org', tz='CET-1CEST,M3.5.0,M10.5.0/3')
    sleep_ms(500) # small delay - trial and error
#'''
# TODO: vanilla micropython
# if no internet connection, try to time from MCP7940 (RTC shield)


# 2019-0801 added from @Jumpero
# https://forum.micropython.org/viewtopic.php?f=2&t=4034
#   Micropython esp8266
#   This code returns the Central European Time (CET) including daylight saving
#   Winter (CET) is UTC+1H Summer (CEST) is UTC+2H
#   Changes happen last Sundays of March (CEST) and October (CET) at 01:00 UTC
#   Ref. formulas : http://www.webexhibits.org/daylightsaving/i.html
#        Since 1996, valid through 2099
def cettime():
    """cettime() - returns localtime in Central European Time (CET)
       including daylight saving. """
    year = time.localtime()[0]       # get current year
    # Time of March change to CEST
    HHMarch = time.mktime((year, 3, (31-(int(5*year/4+4))%7),1,0,0,0,0,0))
    HHOctober = time.mktime((year, 10, (31-(int(5*year/4+1))%7),1,0,0,0,0,0)) #Time of October change to CET
    now = time.time()
    if now < HHMarch:               # we are before last sunday of march
        cet = time.localtime(now+3600)  # CET:  UTC+1H
    elif now < HHOctober:           # we are before last sunday of october
        cet = time.localtime(now+7200)  # CEST: UTC+2H
    else:                            # we are after last sunday of october
        cet = time.localtime(now+3600)  # CET:  UTC+1H
    return(cet)


def timerecord():
    """ timerecord(): returns user-friendly localtime for CES)T timezone.
        example: '2019-08-03, 17:09:26' """
    t = cettime()
    now = '{:04d}-{:02d}-{:02d}, {:02d}:{:02d}:{:02d}'.format(t[0], t[1] ,t[2], t[3], t[4], t[5])
    return now


# 2019-0217 added if __main__
if __name__ == '__main__':
    from rtc_sync import timerecord
    print("It's", timerecord())
