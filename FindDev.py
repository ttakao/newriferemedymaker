#!/usr/bin/env python
# -*- coding: utf-8 ^*-
import sys
import usb.core

sTitle = "USB set"
dev = usb.core.find(find_all=True)
# loop through devices, printing vendor and product ids in decimal and hex
sys.stdout.write("--------------\n")
for cfg in dev:
    sys.stdout.write('VendorID=' + str(cfg.idVendor) + ' & ProductID=' + str(cfg.idProduct) + '\n')
sys.stdout.write("--------------\n")
