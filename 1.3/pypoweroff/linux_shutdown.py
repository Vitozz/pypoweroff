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
        
    def Notify(self, icon,  message):
        bus = dbus.SessionBus()
        try:
                service = 'org.freedesktop.Notifications'
                path = '/org/freedesktop/Notifications'
                iface = 'org.freedesktop.Notifications'
                notify_interface = dbus.Interface(bus.get_object(service, path), iface)
                if notify_interface:
                        list=notify_interface.get_dbus_method('GetCapabilities')()
                        if "body" in list:
                                notify_interface.Notify("PyPowerOff", 0, icon, "Information:", message, '', '', -1)
        except dbus.exceptions.DBusException as error:
                import os
                os.sys.stderr.write("%s\n"%error)
