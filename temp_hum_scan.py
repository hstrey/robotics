import time
import os
import sys
import binascii
import struct
from bluepy import btle

def dump_services(dev):
    services = sorted(dev.getServices(), key=lambda s: s.hndStart)
    for s in services:
        print ("\t%04x: %s" % (s.hndStart, s))
        if s.hndStart == s.hndEnd:
            continue
        chars = s.getCharacteristics()
        for i, c in enumerate(chars):
            props = c.propertiesToString()
            h = c.getHandle()
            if 'READ' in props:
                val = c.read()
                if c.uuid == btle.AssignedNumbers.device_name:
                    string = '\'' + val.decode('utf-8') + '\''
                elif c.uuid == btle.AssignedNumbers.device_information:
                    string = repr(val)
                elif 'NOTIFY' in props:
					sensordata=bytearray(val)
					temp,=struct.unpack('f',sensordata[:4])
					humidity,=struct.unpack('f',sensordata[4:])
					print('temp: ',temp,'humidity: ',humidity)
                else:
                    string = '<s' + binascii.b2a_hex(val).decode('utf-8') + '>'
            else:
                string=''
            print ("\t%04x:    %-59s %-12s %s" % (h, c, props, string))

class ScanPrint(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            status = "new"
        elif isNewData:
            if self.opts.new: return
            status = "update"
        else:
            if not self.opts.all: return
            status = "old"

        print ('    Device (%s): %s (%s), %d dBm %s' % 
                  (status,
                   dev.addr,
                   dev.addrType,
                   dev.rssi,
                   ('' if dev.connectable else '(not connectable)') )
              )
        print

def main():
    scanner = btle.Scanner(0)

    print ("Scanning for devices...")
    devices = scanner.scan(2)

    print devices
    
    for dev in devices:
        print ('    Device: %s (%s), %d dBm' % 
                  (dev.addr,
                   dev.addrType,
                   dev.rssi)
              )

        for (sdid, desc, val) in dev.getScanData():
            print('sdid: ',sdid,'desc: ',desc, 'val: ',val)
            if sdid in [8,9]:
                print ('\t' + desc + ': \'' + val + '\'')
            else:
                print ('\t' + desc + ': <' + val + '>')

        if not dev.connectable:

            continue

        print ("    Connecting to", dev.addr + ":")

        d = btle.Peripheral(dev)
        dump_services(d)
        d.disconnect()
        print

if __name__ == "__main__":
    main()






