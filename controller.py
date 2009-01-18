#
#  controller.py
#  Album Sound Check
#
#  Created by Scott Robertson on 1/17/09.
#  Copyright (c) 2009 __MyCompanyName__. All rights reserved.
#

from objc import YES, NO, IBAction, IBOutlet
from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper
from soundcheck import SoundCheck
import os, os.path, re, math

class controller(NSWindowController):

    text = IBOutlet()
    tableView = IBOutlet()

    stuff = []
    l_avg = 0
    r_avg = 0

    def awakeFromNib(self):
        self.text.setStringValue_("")

# NSTableDataSource

    def numberOfRowsInTableView_(self, aTableView):
        return len(self.stuff)

    def tableView_objectValueForTableColumn_row_(self, aTableView,
            aTableColumn, rowIndex):
        return self.stuff[rowIndex][aTableColumn.identifier()]

    def tableView_setObjectValue_forTableColumn_row_(self, aTableView,
            anObject, aTableColumn, rowIndex):
        self.stuff[rowIndex][aTableColumn.identifier()] = anObject
        if aTableColumn.identifier() == 'use':
            self.generateAverage()

    @IBAction
    def apply_(self, sender):
        setfor = [x for x in self.stuff if x['apply'] == YES]

    def loadDir(self, dirname):
        self.stuff = []
        ok_files = []
        for root, dirs, files in os.walk(dirname):
            ok_files += [os.path.join(root, n) for n in files \
                    if (re.match(r'.*(\.mp3|\.m4a|\.m4p|\.mp4)$', n))]
        for file in ok_files:
            hash = {}
            hash['obj'] = SoundCheck(file)
            hash['use'] = YES
            hash['apply'] = YES
            hash['file'] = os.path.basename(file)
            hash['db'] = "%+.2f, %+.2f" % (hash['obj'].dB[0], hash['obj'].dB[1])
            self.stuff.append(hash)
        self.tableView.reloadData()
        self.generateAverage()

    def generateAverage(self):
        self.l_avg, self.r_avg = (0, 0)
        use = [x['obj'].dB for x in self.stuff if x['use'] == YES]
        if len(use) > 0:
            left = [x[0] for x in use]
            right = [x[1] for x in use]
            self.l_avg = sum(left)/len(left)
            self.r_avg = sum(right)/len(right)
        self.text.setStringValue_("%+.2f dB, %+.2f dB" % (self.l_avg, self.r_avg))

# Open panel
    @IBAction
    def open_(self, sender):
        panel = NSOpenPanel.openPanel()
        panel.setCanChooseDirectories_(YES)
        panel.setAllowsMultipleSelection_(NO)
        panel.beginSheetForDirectory_file_types_modalForWindow_modalDelegate_didEndSelector_contextInfo_(
                "~/Music/iTunes/iTunes Music/", None, [], NSApp().mainWindow(),
                self, 'openPanelDidEnd:panel:returnCode:contextInfo:', 0)

    @AppHelper.endSheetMethod
    def openPanelDidEnd_panel_returnCode_contextInfo_(self, panel, returnCode,
            contextInfo):
        if returnCode:
            self.loadDir(panel.filenames()[0])
