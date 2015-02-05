myFileName = "./main.py"  # TODO: used to source itself when changed


def printOut(s):
    with open('main.log', 'a') as f:
        f.write(str(s) + '\n')


# ==========8<========== You don't need to edit until the next marker
# TODO: this should be a separate module BTW

import gdb
import os.path


allBreaks = []


class BreakAndContinue(gdb.Breakpoint):
    def __init__(self, what):
        super(BreakAndContinue, self).__init__(what)
        self.silent = True
        self.lastModTime = os.path.getmtime(myFileName)
        allBreaks.append(self)

    def executeOnStop(self, name):
        printOut("Pls override me! KTHX!")

    def stop(self):
        if self.lastModTime < os.path.getmtime(myFileName):
            for i in allBreaks:
                i.disableBp()
            # TODO: this is ugly! Note: an example how to run gdb commands
            gdb.execute('python execfile("' + myFileName + '")')
        frameName = gdb.selected_frame().name()
        if frameName.find('@plt') >= 0:
            return False
        self.executeOnStop()
        return False

    def disableBp(self):
        self.enabled = False


class WatchWithContext(BreakAndContinue):
    def __init__(self, enterScope, exitScope, toWatch, Wtype=gdb.BP_WATCHPOINT):
        super(WatchWithContext, self).__init__(enterScope)
        self.enterScope = enterScope
        self.toWatch = toWatch
        self.Wtype = Wtype
        self.watch = []

        class RemoveBp(BreakAndContinue):
            def __init__(self, exitScope, enter):
                super(RemoveBp, self).__init__(exitScope)
                self.enter = enter

            def executeOnStop(self):
                address = gdb.parse_and_eval(self.enter.toWatch)
                for i in self.enter.watch:
                    if address == i[0]:
                        i[1].enabled = False
                return False

        self.rm = RemoveBp(exitScope, self)

    def executeOnStop(self):
        class WP(gdb.Breakpoint):
            def __init__(self, toWatch, enter):
                super(WP, self).__init__(toWatch, type=enter.Wtype)
                self.enter = enter

            def stop(self):
                self.enter.doOnWatch(self)
                return False

        address = gdb.parse_and_eval(self.toWatch)
        i = WP('*(int*) ' + str(address.address), self)  # TODO: WTF?
        self.watch.append((address, i))

    def doOnWatch(self, wp):
        try:
            v = gdb.parse_and_eval(self.toWatch)
            printOut('[Override me!] New value: ' + str(v))
        except:
            frameName = gdb.selected_frame().name()
            printOut('TODO: fix WP error: ' + frameName + '!' + self.toWatch)
            wp.enabled = False

    def disableBp(self):
        # TODO: in some cases, this should a no-op, i.e. for singletons, etc
        for i in self.watch:
            i[1].enabled = False
        self.rm.enabled = False
        self.enabled = False

# ==========8<========== next marker


class CsFun(BreakAndContinue):
    def executeOnStop(self):
        try:
            self.i += 1
        except:
            self.i = 0
        if (self.i % 999 == 0):
            printOut(gdb.parse_and_eval("i"))


def gdbMain():
    #gdb.execute('quit')
    CsFun("funner")
    WatchWithContext('Base::Base', 'Base::~Base', 'i')
    WatchWithContext('mainLoop.cpp:10', 'mainLoop.cpp:12', 'w')
    pass

gdbMain()
