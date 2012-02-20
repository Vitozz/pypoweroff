#!/usr/bin/env python
# -*- mode: python; coding: koi8-r -*-

import dbus

class Shutdowner:
    def __init__(self):
        self.bus = dbus.SystemBus()
        self.manager = self.bus.get_object('org.freedesktop.ConsoleKit', '/org/freedesktop/ConsoleKit/Manager')
        self.ConsoleKit = dbus.Interface(self.manager, 'org.freedesktop.ConsoleKit.Manager')

    def Shutdown(self):
        if bool(self.ConsoleKit.get_dbus_method('CanStop')()):
            self.ConsoleKit.get_dbus_method('Stop')()
            return True
        return False

    def Reboot(self):
        if bool(self.ConsoleKit.get_dbus_method('CanRestart')()):
            self.ConsoleKit.get_dbus_method('Restart')()
            return True
        return False
