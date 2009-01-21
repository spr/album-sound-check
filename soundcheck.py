#
#  soundcheck.py
#  Album Sound Check
#
#  Created by Scott Robertson on 1/17/09.
#  Copyright (c) 2009 __MyCompanyName__. All rights reserved.
#

from __future__ import division
from mutagen.mp3 import MP3
import tag_wrapper
import math
from Foundation import NSLog

class SoundCheck(object):
    def __init__(self, file):
        self.tag = tag_wrapper.tag(file)
        if type(self.tag._tag) == MP3:
            self.field = 'iTunNORM'
        else:
            self.field = '----:com.apple.iTunes:iTunNORM'
        if self.field not in self.tag.keys():
            NSLog("Missing Field: %s" % self.tag.keys())
            self.sc1000 = (0,0)
            self.sc2500 = (0,0)
            self.so = (0,0)
            self.peak = (0,0)
            self.st = (0,0)
        else:
            parts = self.get_parts()
            self.sc1000 = (parts[0], parts[1])
            self.sc2500 = (parts[2], parts[3])
            self.so = (parts[4], parts[5])
            self.peak = (parts[6], parts[7])
            self.st = (parts[8], parts[9])

    def soundcheck2db(self, sc, gain):
        if sc == 0:
            return 0.0
        return -10 * math.log10(sc/gain)
    
    def db2soundcheck(self, db, gain):
        return int(gain * math.pow(10, -db/10))

    def get_parts(self):
        return [int(x,16) for x in self.tag[self.field][0].split()]

    def build_from_parts(self):
        str = ""
        for x in (self.sc1000 + self.sc2500 + self.so + self.peak + self.st):
            s = hex(x)[2:].upper()
            s = ("0" * (8 - len(s))) + s
            str = " ".join((str, s))
        return str

    def getdB(self):
        return (self.soundcheck2db(self.sc1000[0], 1000),
                self.soundcheck2db(self.sc1000[1], 1000))

    def setdB(self, value):
        self.sc1000 = (self.db2soundcheck(value[0], 1000),
                self.db2soundcheck(value[1], 1000))

    dB = property(getdB, setdB)

    def getdB_2500(self):
        return (self.soundcheck2db(self.sc2500[0], 2500),
                self.soundcheck2db(self.sc2500[1], 2500))

    def setdB_2500(self, value):
        self.sc2500 = (self.db2soundcheck(value[0], 2500),
                self.db2soundcheck(value[1], 2500))

    db2500 = property(getdB_2500, setdB_2500)

    def save(self):
        self.tag[self.field] = self.build_from_parts()
        self.tag.save()
