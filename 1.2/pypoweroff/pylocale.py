#!/usr/bin/python
# -*- coding: utf-8 -*-
import locale
import os
from ConfigParser import ConfigParser

class MyLocale:
    def __init__(self):
        """Locale chooser for PowerOff Tool"""
        self.main_dic = {'timerid1': '',  'timerid2': '',  'timespin': '',  'label1': '', 
                                'label3': '',  'rebootlabel': '',  'reboothint': '',  'shutdownlabel': '',
                                'shutdownhint': '',  'poffbutton': '',  'title': '',  'cantitle': '', 
                                'tmpsec': '',  'author': '',  'comments': '',  'website': ''}
        self.menu_dic = {'fileitem': '',  'settingsitem': '',  'helpitem': ''}
        self.tray_dic ={'restorehide': '',  'restore': '',  'tooltip': 'tooltip'}
        self.dialog_dic = {'exitlabel': '',  'attentionp1': '',  'attentionp2': '',  'typestringsh': '', 
                                'typestringrb': ''}
        self.CP = ConfigParser()
        curr_locale = locale.getlocale()[0][0:2]
        self.localepath = "/usr/share/pypoweroff/lang/%s.lng"%curr_locale
        if os.path.exists(self.localepath):
            self.localepath =  "/usr/share/pypoweroff/lang/"+"%s.lng"%curr_locale
        else:
            self.localepath = None
        if self.localepath:
            self.CP.read(self.localepath)
            self.getLocale()
        else:
            self.setDefault()
        
    def getLocale(self):
            #Main
            self.main_dic['title'] = str(self.CP.get('Main',  'title'))
            self.main_dic['timerid1'] = str(self.CP.get('Main',  'timerid1'))
            self.main_dic['timerid2'] =str(self.CP.get('Main',  'timerid2'))
            self.main_dic['timespin'] = str(self.CP.get('Main',  'timespin'))
            self.main_dic['label1'] = str(self.CP.get('Main',  'label1'))
            self.main_dic['label3'] = str(self.CP.get('Main',  'label3'))
            self.main_dic['rebootlabel'] = str(self.CP.get('Main',  'rebootlabel'))
            self.main_dic['reboothint'] = str(self.CP.get('Main',  'reboothint'))
            self.main_dic['shutdownlabel'] = str(self.CP.get('Main',  'shutdownlabel'))
            self.main_dic['shutdownhint'] = str(self.CP.get('Main',  'shutdownhint'))
            self.main_dic['poffbutton'] = str(self.CP.get('Main',  'poffbutton'))
            self.main_dic['cantitle'] = str(self.CP.get('Main',  'cantitle'))
            self.main_dic['tmpsec'] = str(self.CP.get('Main',  'tmpsec'))
            self.main_dic['author'] = str(self.CP.get('Main',  'author'))
            self.main_dic['comments'] = str(self.CP.get('Main',  'comments'))
            self.main_dic['website'] = str(self.CP.get('Main',  'website'))
            #Menu
            self.menu_dic['fileitem'] = str(self.CP.get('Menu',  'fileitem'))
            self.menu_dic['settingsitem'] = str(self.CP.get('Menu',  'settingsitem'))
            self.menu_dic['helpitem'] = str(self.CP.get('Menu',  'helpitem'))
            #Dialog
            self.dialog_dic['exitlabel'] = str(self.CP.get('Dialog',  'exitlabel'))
            self.dialog_dic['attentionp1'] = str(self.CP.get('Dialog',  'attentionp1'))
            self.dialog_dic['attentionp2'] = str(self.CP.get('Dialog',  'attentionp2'))
            self.dialog_dic['typestringsh'] = str(self.CP.get('Dialog',  'typestringsh'))
            self.dialog_dic['typestringrb'] = str(self.CP.get('Dialog',  'typestringrb'))
            #Tray
            self.tray_dic['restorehide'] = str(self.CP.get('Tray',  'restorehide'))
            self.tray_dic['restore'] = str(self.CP.get('Tray',  'restore'))
            self.tray_dic['tooltip'] = str(self.CP.get('Tray',  'tooltip'))
            
    def setDefault(self):
            self.main_dic['title'] = "Power Off Tool"
            self.main_dic['timerid1'] = "Time to shutdown (min)"
            self.main_dic['timerid2'] = "Shutdown in (hour:min)"
            self.main_dic['timespin'] = "Time to shutdown/reboot"
            self.main_dic['label1'] = "Hours"
            self.main_dic['label3'] = "Minutes"
            self.main_dic['rebootlabel'] = "Reboot"
            self.main_dic['reboothint'] = "Reboot system"
            self.main_dic['shutdownlabel'] = "Shutdown"
            self.main_dic['shutdownhint'] = "Shutdown system"
            self.main_dic['poffbutton'] = "Shutdown/Reboot"
            self.main_dic['cantitle'] = "Operation cancelled"
            self.main_dic['tmpsec'] = "Time to shutdown"
            self.main_dic['author'] = "Vitaly Tonkacheyev"
            self.main_dic['comments'] = "The program for the planned shutdown of the computer for Linux and Windows"
            self.main_dic['website'] = "Program Website"
            #Menu
            self.menu_dic['fileitem'] = "File"
            self.menu_dic['settingsitem'] = "Options"
            self.menu_dic['helpitem'] = "Help"
            #Dialog
            self.dialog_dic['exitlabel'] = "Do you really want to quit this program?"
            self.dialog_dic['attentionp1'] = "Do you really want to"
            self.dialog_dic['attentionp2'] = " your computer after"
            self.dialog_dic['typestringsh'] = "shutdown"
            self.dialog_dic['typestringrb'] = "reboot"
            #Tray
            self.tray_dic['restorehide'] = "Hide"
            self.tray_dic['restore'] = "Restore"
            self.tray_dic['tooltip'] = "Power Off Tool"
            
