#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
try:
    import pygtk
    pygtk.require('2.0')
    import gtk
except:
    sys.stderr.write('No Gtk Module Found')
    sys.exit(1)

class StatusIcc:
    # activate callback
    def on_hide_resore(self, widget, data=None):
        self.onLClick(widget)

    # popup callback
    def popup(self, widget, button, time, data=None):
        if button == 3:
            if data:
                data.show_all()
                data.popup(None, None, None, 3, time)

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


    def __init__(self, parent):
        self.parent = parent
        # create a new Status Icon
        self.staticon = gtk.StatusIcon()
        #create Popup-menu
        self.menu = gtk.Menu()
        #Restore
        self.restoreItem = gtk.ImageMenuItem(gtk.STOCK_GO_UP)
        self.restoreItem.connect('activate', self.on_hide_resore)
        self.menu.append(self.restoreItem)
        self.restoreItem.get_children()[0].set_label(self.parent.language.tray_dic.get('restorehide'))
        separator1 = gtk.SeparatorMenuItem()
        self.menu.append(separator1)
        #Mixer
        self.cancelitem = gtk.ImageMenuItem(gtk.STOCK_CANCEL)
        self.cancelitem.connect('activate', self.onAbort)
        self.menu.append(self.cancelitem)
        separator2 = gtk.SeparatorMenuItem()
        self.menu.append(separator2)
        #About
        self.aboutItem = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        self.aboutItem.connect('activate', self.onAbout)
        self.menu.append(self.aboutItem)
        #Quit
        self.quitItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        self.quitItem.connect('activate', self.onQuit, self.staticon)
        self.menu.append(self.quitItem)
        #
        if self.parent.systype == "windows":
            self.staticon.set_from_file("images\\poweroff.ico")
        else:
            self.staticon.set_from_file(self.parent.loader.get("pypoweroff", "images/tb_icon.png"))
        self.status_tooltip = self.parent.language.tray_dic.get('tooltip')
        self.staticon.set_tooltip(self.status_tooltip)
        self.staticon.connect('activate', self.onLClick)
        self.staticon.connect('popup_menu', self.popup, self.menu)
        self.staticon.set_visible(True)
        self.cancelitem.set_sensitive(False)
