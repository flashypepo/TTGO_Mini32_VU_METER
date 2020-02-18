"""
boot.py: this file is executed on every boot (including wake-boot from deepsleep)

2019-1130 Wifi activated
2018-1008 pepo - tried to startup Wifi connection
    * WifiManager and wificonfig.json
    * added rtc sync with NTP-server
    ERROR: includes are not found, sys.path ???
"""
import gc

USE_WIFI = False  # 2020-0218

if USE_WIFI is True:
    # ''' create Wifi object
    import wifimanager
    wifi = wifimanager.WifiManager("config/wificonfig.json")
    # connect to Wifi network
    wifi.connect()
    # device IP
    print('[boot.py] Device IP: {0}'.format(wifi._wlan.ifconfig()[0]))
    # RTC sync
    # 2019-1130 replaced: import rtc_sync
    from rtc_sync import rtc, timerecord
    boottime = timerecord()
    print("It's", boottime)
    rtc.memory('Boot time was ' + boottime)

    # Change password for telnet, ftp..
    # 2018-1007 TODO: wifi.change_access('pepo', 'plasma')

    # print MAC-address
    print('[boot.py] MAC:', wifi.mac)

# cleanup
gc.collect()
print('[boot.py] mem_free = {} bytes'.format(gc.mem_free()))
