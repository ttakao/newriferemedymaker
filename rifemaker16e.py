#!/usr/bin/env python
# -*- coding: utf-8 ^*-
'''
Name: Energy Remedy Manager  Version 1.6

Functions:
1. Read specified "Scenario" file.
2. User can choose "Scenario"s.
3. Specify Frequency generation time and interval time.
4. Run Scenarios
5. Coversation with Function Generator by SCPI via USB.
6. End Alert.
7. Go back to 2.

Module structure:
A. Executer
B. UX manager

Required Package:
- PyUSB
- easyGUI
- csv

(libusb-win32 is needed as USB driver.)

All Rights Reserved by Mind Craft Ltd. 2017.
2017/03/06 First Relase.
2017/03/19 remove noise
2017/03/22 use codecs file i/o
2017/03/29 After end of scenario, ask if continue or not.
2019/04/03 easygui choicebox
2019/11/23 for culcurating x1000, use decimal instead of float

'''
from easygui import *
from decimal import *
import codecs
import usb.core
import usb.util
import sys
import os.path
import configparser
import time
import winsound
import re

global dev
global cfg
global itfs
global ep_out
global ep_in
global interval

def SCPIcmd(cmd):
    global dev
    global cfg
    global itfs
    global ep_out
    global ep_in

    # comannd shuld be reduced
    

    print(cmd,end=":")
    ep_out.write(cmd+"\n")

    OKSign = "- > \n" # for decode

    ret = ep_in.read(64)
    chars = " ".join(map(chr,ret))

    if OKSign in chars:
        chars = "OK\n"

    print(chars)
    
def InitSCPI(vender, product):
    global dev
    global cfg
    global itfs
    global ep_out
    global ep_in
    
    dev = usb.core.find(idVendor=int(vender), idProduct=int(product))

    if dev is None:
        raise ValueError('Device not found')
        sys.exit()

    dev.set_configuration()

    cfg = dev.get_active_configuration()

    itfs = cfg[(0,0)]

    ep_out = usb.util.find_descriptor(
            itfs,
            custom_match = \
            lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_OUT)

    ep_in = usb.util.find_descriptor(
            itfs,
            custom_match = \
            lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_IN)

    SCPIcmd("*IDN?")
    SCPIcmd("*RST")
    time.sleep(3)
    SCPIcmd(":FUNC:SQU:AMPL 5")

def ExecSCPI(freqs):

    global interval

    print("debug:"+freqs+","+interval)
        
    SCPIcmd(":CHAN:CH1 ON")

    for f in freqs.split(','):

        if re.compile("^\d+\.?\d*\Z").match(f):
            f_num = Decimal(f) * 1000
            command = ":FUNC:SQU:FREQ " + str(f_num)
            
            SCPIcmd(command)
            time.sleep(int(interval))

    SCPIcmd(":CHAN:CH1 OFF")

if __name__ == "__main__":

#----- Ini process
# 1. Check ini file.
# 2. If exists, read 
# 3. If not found, show dialog and check USB validity.
# 4. Write down into ini file.
#
    sTitle = "Energy Remedy Manager V1.6e"
    configfile = "./config.ini"
    config = configparser.ConfigParser()
        
    if os.path.isfile(configfile):
        config.read(configfile)
        VenderID = config['DEFAULT']['VenderID']
        ProductID = config['DEFAULT']['ProductID']
        interval = config['DEFAULT']['interval']
        print( 'Interval='+interval)
        InitSCPI(VenderID, ProductID)
    else:
        raise ValueError('config.ini not found')
        sys.exit()


# ------ Read scnario and process
# 1. propt file selection
# 2. read and show dialog
# 4. Do it.

    while True:
        msg = "Please choose Rife Frequency list file."
        filetype=["*.csv"]
        default="*.csv"
        multiple=False
        FileName = fileopenbox(msg,sTitle,default,filetype,multiple)

        if FileName is None:
            raise ValueError('Scenario file not set.')
            sys.exit()
        titles = []
        csvfile = codecs.open(FileName,'r','utf-8')
        for line in csvfile:
            if line.find('\t'):
                list = line.split('\t')
                ename = list[0].strip('"')
                #print(ename)
                jname = list[1].strip('"')
                #print(jname)
                freqs = list[2].strip('"')
                #print(freqs)

                titles.append(jname+"|"+ename+"|"+freqs)

        csvfile.close()

        selected = choicebox(msg='Please choose remedy name.',title='Chooseing Remedy',choices=titles)

        if selected != None:
            elements = selected.split("|")
            ExecSCPI(elements[2])
            winsound.Beep(880,2000)

        if ynbox("Will you make other Remedy？"):
            pass
        else:
            break
        
    sys.exit()

