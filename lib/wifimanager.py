"""
wifimanager.py - connects to Wifi networks
* JSON-based

2019-0801 PePo micropython 1.11, removed IDENTITY, add board

Format 'wificonfig.json':
{
    "STATIC_IP": "None",            # or, "145.45.16.2" for STATIC IP
    "SUBNET" : "your subnet IP",    # example: "192.168.178.0"
    "GATEWAY_IP": "your gateway IP",# example: "192.168.178.1"
    "MASKER": "your mask",          # example: "255.255.255.0",
    "SSID": "your ssid",            # example: "devices"
    "PASSWRD" : "your password",    # example WF: "devices2"
    "DNS": "8.8.8.8"                # example Google DNS
}

"""
from network import STA_IF, WLAN
from machine import idle
import json
import time
from ubinascii import hexlify

# configurations
# DEBUG or not debug
USE_DEBUG = False


class WifiManager:

    def __init__(self, jsonfile):
        # Load Wifi configuration from JSON file.
        self._config = self.readjson(jsonfile)
        # create network in STAtion mode
        self._wlan = WLAN(STA_IF)

    def connect(self):
        """connect() - connects device according to network parameters
           in config-file."""
        # check if network is connected. If yes: return, finished
        # 2019-0801 changed: if self._wlan.isconnected():
        if self.isconnected:
            if USE_DEBUG:
                print('WLAN already connected')
            return self._wlan.ifconfig()

        # activate Wifi interface
        if self._wlan.active() is False:
            self._wlan.active(True)
        # scan available networks for the required one
        nets = self._wlan.scan()
        for net in nets:
            ssid = net[0]
            if ssid == bytearray(self._config['SSID']):  # must use bytearray!
                if USE_DEBUG:
                    print("Startup WiFi ..." + self._config['SSID'])
                # specify if static or dynamic IP is requested
                # STATIC IP: an IP is given
                # DYNAMIC IP: None
                if self._config['STATIC_IP'] is not '':
                    if USE_DEBUG:
                        print('WifiManager::Static IP configuration')
                    # configure network for static IP
                    self._wlan.ifconfig((self._config['STATIC_IP'],
                                         self._config['MASKER'],
                                         self._config['GATEWAY_IP'],
                                         self._config['DNS']))

                # connect to SSID... either for STATIC or DYNAMIC IP
                self._wlan.connect(self._config['SSID'],
                                   self._config['PASSWRD'])
                while not self.isconnected:
                    idle()  # save power while waiting
                    time.sleep_ms(100)  # give it some time
                if USE_DEBUG:
                    print("Network '{}' connection succeeded!".format(ssid))
                break

        # check connection, if not succesfull: raise exception
        if not self._wlan.active():
            raise exception('Network {0} not found.'.format(ssid))

        # returns network configuration...
        # although 'myPy.local' should work on MacOS X (Bonjour)
        return self._wlan.ifconfig()

    def readjson(self, jsonfile):
        """readjson(file) - returns the contents of a JSON file"""
        with open(jsonfile, 'r') as infile:
            config = json.load(infile)
        return config

    def print_config(self):
        """print_config() - print config data on screen."""
        for key in self._config.keys():
            print('[{0}] = {1}'.format(key, self._config[key]))

    # wrapper for network scan
    def scan(self):
        """scan() - Performs a network scan and returns a list
        of named tuples with (ssid, bssid, sec, channel, rssi)
        """
        if self.isconnected is False:
            return False
        nets = self._wlan.scan()
        nets_list = {}
        for net in nets:
            nets_list['SSID'] = str(net[0], 'utf8')
            # nets_list['bssid'] = str(net[1])
            nets_list['CHANNEL'] = str(net[2])
            nets_list['RSSI'] = str(net[3]) + ' dBm'
            nets_list['SECURITY'] = self._get_secure(net[4])
            print(nets_list)

    def _get_secure(self, num):
        security = [
            'Open Wifi',   # 0
            'WEP',         # 1
            'WPA-PSK',     # 2
            'WPA2-PSK',    # 3
            'WPA/WP2-PSK'  # 4
        ]
        if num < len(security):
            return security[num]
        else:
            return str(num)

    def disconnect(self):
        """disconnect() - disconnect the Wifi connection"""
        self._wlan.disconnect()
        time.sleep_ms(50)  # give it time, trial-and-error value
        return self.isconnected

    @property
    def isconnected(self):
        """isconnected() - returns True when device is connected to wifi,
        else False """
        return self._wlan.isconnected()

    @property
    def mac(self):
        """returns MAC-address of device"""
        mac = hexlify(WLAN().config('mac'), ':').decode()
        return mac.upper()  # MAC-address in upper case


# test/usage
if __name__ == '__main__':
    from wifimanager import WifiManager
    wifi = WifiManager("wificonfig.json")
    print('MAC address= {}'.format(wifi.mac))
    params = wifi.connect()
    print('Device IP is {0}'.format(params[0]))  # device IP
    # wifi.print_config()
