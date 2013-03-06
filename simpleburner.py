#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Copyright (C) 2009-2013 sirmacik
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import os
import sys
import subprocess
from optparse import OptionParser

def programcheck():
    print "Looking for cdrkit..."
    if os.path.exists('/usr/bin/wodim') and os.path.exists('/usr/bin/genisoimage'):
        globals() ["writer"] = 'wodim'
        globals() ["isomaker"] = 'genisoimage'
        print "[OK]"

    else:
        print >>sys.stderr, "Not found\nLooking for cdrtools..."
        if os.path.exists('/usr/bin/cdrecord') and os.path.exists('/usr/bin/mkisofs'):
            globals() ["writer"] = 'cdrecord'
            globals() ["isomaker"] = 'mkisofs'
            print "[OK]"
        else:
            print >>sys.stderr, "Not found: Please install cdrkit or cdrtools!"
            sys.exit(1)
def optcheck():
    if not burn:
        if not datadir:
            print >>sys.stderr, "Failed! You must deine --data option."
            sys.exit(1)
        elif not os.path.exists(datadir):
            print >>sys.stderr, "Failed! Directory \"%s\" does not exist!" % (datadir)
            sys.exit(1)
def makeiso():
    print "Making iso image..."
    command = "%s -U -quiet -o %s \"%s\"" % (isomaker, isoname, datadir)
    makeiso = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]
    if makeiso:
        print >>sys.stderr, "Failed!"
        sys.exit(1)
    else:
        print "[OK]\nFile stored in %s" % isoname
def burniso():
    print "Burning iso..."
    if speed:
        burnspeed = " --speed=%s" % speed
    else:
        burnspeed = ''
    if test == "True":
        runtest = ' --dummy'
    else:
        runtest = ''
    command = "%s --eject -vs -%s --dev=%s %s %s %s" % (writer, mode, device, burnspeed, runtest, isoname)
    burniso = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]
    if burniso:
        print >>sys.stderr, "Failed or ended successfully with warnings"
        sys.exit(1)
    else:
        print "[OK]"

if __name__=="__main__":
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("--data", dest="datadir",
                      help="set directory with data to burn")
    parser.add_option("--name", dest="isoname", default="/tmp/cd.iso",
                      help="set path and/or name of iso image (by default /tmp/cd.iso)")
    parser.add_option("--device", dest="device", default="/dev/sr0",
                      help="set device to use (default /dev/sr0)")
    parser.add_option("--speed", dest="speed",
                      help="set burn speed (by default it will be autodetected)")
    parser.add_option("--mode", dest="mode", default="tao",
                      help="set burn mode; available options are: TAO (default), DAO, SAO, RAW)")
    parser.add_option("-t", "--test", action="store_true", dest="test", default= False ,
                      help="run in test burn mode")
    parser.add_option("-b", "--burn-only", action="store_true", dest="burn", default=False,
                      help="run without making iso image")
    parser.add_option("-m", "--makeiso", action="store_true", dest="make", default=False,
                      help="make only iso image")

    (options, args) = parser.parse_args()
    datadir = options.datadir
    isoname = options.isoname
    device = options.device
    speed = options.speed
    mode = options.mode
    test = options.test
    burn = options.burn
    make = options.make

    programcheck()
    optcheck()
    if burn == True:
        burniso()
    elif make == True:
        makeiso()
    else:
        makeiso()
        burniso()
        
