#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
from gi.repository import Gtk

class StatusIcc:
    # activate callback
    def on_hide_resore(self, widget, data=None):
        self.onLClick(widget)

    # popup callback
    def popup(self, widget, button, time, data=None):
        if button == 3:
            if data:
                data.show_all()
                data.popup(None, None, None, None, button, time)
                return True
        return False

    def onLClick(self, widget, data=None):
        self.parent.OnHide()

    def onQuit(self, widget, data=None):
        print ("Saving settings...")
        self.parent.OnExit(widget)

    def onAbort(self, widget, data=None):
        if self.parent:
            self.parent.OnCancel(widget)

    def onAbout(self, widget, data=None):
        if self.parent:
            self.parent.OnAbout(widget)

    def onShutdown(self, widget, data=None):
        if self.parent:
            self.parent.OnShutdownNow(widget)

    def onReboot(self, widget, data=None):
        if self.parent:
            self.parent.OnRebootNow(widget)

    def __init__(self, parent):
        """Status icon creation class"""
        self.parent = parent
        # create a new Status Icon
        self.staticon = Gtk.StatusIcon()
        #create Popup-menu
        self.menu = Gtk.Menu()
        #Restore
        self.restoreItem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_GO_UP,  None)
        self.restoreItem.connect('activate', self.on_hide_resore)
        self.menu.append(self.restoreItem)
        self.restoreItem.get_children()[0].set_label(self.parent.language.tray_dic.get('restorehide'))
        separator1 = Gtk.SeparatorMenuItem()
        self.menu.append(separator1)
        #Mixer
        self.cancelitem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_CANCEL, None)
        self.cancelitem.connect('activate', self.onAbort)
        self.menu.append(self.cancelitem)
        separator2 = Gtk.SeparatorMenuItem()
        self.menu.append(separator2)
        #About
        self.aboutItem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_ABOUT,  None)
        self.aboutItem.connect('activate', self.onAbout)
        self.menu.append(self.aboutItem)
        separator3 = Gtk.SeparatorMenuItem()
        self.menu.append(separator3)
        #Shutdown
        self.shutdownItem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_STOP,  None)
        self.shutdownItem.connect('activate', self.onShutdown)
        self.menu.append(self.shutdownItem)
        self.shutdownItem.get_children()[0].set_label("Shutdown")
        #Reboot
        self.rebootItem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_REFRESH,  None)
        self.rebootItem.connect('activate', self.onReboot)
        self.menu.append(self.rebootItem)
        self.rebootItem.get_children()[0].set_label("Reboot")
        separator4 = Gtk.SeparatorMenuItem()
        self.menu.append(separator4)
        #Quit
        self.quitItem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_QUIT,  None)
        self.quitItem.connect('activate', self.onQuit, self.staticon)
        self.menu.append(self.quitItem)
        #
        if self.parent.systype == "windows":
            self.staticon.set_from_file("images\\poweroff.ico")
        else:
            self.staticon.set_from_file(self.parent.loader.get("pypoweroff", "images/tb_icon.png"))
        self.status_tooltip = self.parent.language.tray_dic.get('tooltip')
        self.staticon.set_tooltip_text(self.status_tooltip)
        self.staticon.connect('activate', self.onLClick)
        self.staticon.connect('popup_menu', self.popup, self.menu)
        self.staticon.set_visible(True)
        self.cancelitem.set_sensitive(False)
