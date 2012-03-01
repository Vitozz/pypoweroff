#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
from ConfigParser import ConfigParser

class OptWork:
    def __init__(self):
        self.settings = {'timeout': None, 'typeoff': None, 'pofWay': None,'htime': None, 'mtime': None, 'lang_id': None}
        self.CP = ConfigParser()
        if str(os.sys.platform) != 'win32':
            self.cfgpath = os.environ["HOME"] + "/.config/pypoweroff/config.cfg"
            if not os.path.exists(self.cfgpath):
                tmpath = os.environ["HOME"] + "/.config/pypoweroff"
                os.mkdir(tmpath, 0o775)
                self.WriteDefaultConfig(self.cfgpath)
        else:
            self.cfgpath = "config.cfg"
            if not os.path.exists(self.cfgpath):
                self.WriteDefaultConfig(self.cfgpath)
                
        self.CP.read(self.cfgpath)

    def GetSettings(self):
        self.settings['timeout']=self.CP.getint('Main', 'timeout')
        self.settings['typeoff']=self.CP.getint('Main', 'typeoff')
        self.settings['htime']=self.CP.getint('Main', 'htime')
        self.settings['mtime']=self.CP.getint('Main', 'mtime')
        self.settings['pofWay']=self.CP.getint('Main', 'pofway')
        self.settings['lang_id']=self.CP.getint('Language', 'id')

    def WriteDefaultConfig(self, confpath):
        f = open(confpath, "wb")
        f.write("[Main]\npofway = 1\nhtime = 0\ntimeout = 0\nmtime = 0\ntypeoff = 0\n[Language]\nid = 0\n")
        f.close()

    def SetSettings(self, Lang_id, timeout, typeoff, htime, mtime, pofWay):
        """ Writes configuration to config file
            args are(self, isRememberLastSettings,
            isRememberPassword, LanguageID)"""
        self.CP.set('Main', 'timeout', str(timeout))
        self.CP.set('Main', 'typeoff', str(typeoff))
        self.CP.set('Main', 'htime', str(htime))
        self.CP.set('Main', 'mtime', str(mtime))
        self.CP.set('Main', 'pofway', str(pofWay))
        #
        if Lang_id == 0:
            self.CP.set('Language', 'id', '0')
        elif Lang_id == 1:
            self.CP.set('Language', 'id', '1')

    def WriteConfig(self):
        #write
        with open(self.cfgpath, 'wb') as configfile:
            self.CP.write(configfile)
