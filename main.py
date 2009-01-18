#
#  main.py
#  Album Sound Check
#
#  Created by Scott Robertson on 1/17/09.
#  Copyright __MyCompanyName__ 2009. All rights reserved.
#

#import modules required by application
import objc
import Foundation
import AppKit
import math, sys, os, os.path, re, __future__
import mutagen, mutagen.mp3, tag_wrapper
import controller
import soundcheck

from PyObjCTools import AppHelper

# import modules containing classes required to start application and load MainMenu.nib
import Album_Sound_CheckAppDelegate

# pass control to AppKit
AppHelper.runEventLoop()
