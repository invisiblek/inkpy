#!/usr/bin/env python3

from bluepy import btle

def getbbqdevices():
  global device
  count = 0
  scanner = btle.Scanner()

  for d in scanner.scan(2):
    if d.getValueText(9) == "iBBQ":
      print("Found {}: {}".format(d.getValueText(9), d.addr))

getbbqdevices()
