#-*- coding: utf-8 -*-

import os, threading
from gi.repository import Gtk, GObject, Gdk, GdkPixbuf
import time, string
from .reswork import loadResFile
from .options import OptWork
from .pytrayIcon import StatusIcc
from .pylocale import MyLocale

MAX_TIME=int(24*3600)
PROJECT="pypoweroff"
VERSION="1.3.1"

if str(os.sys.platform) != "win32":
    from .linux_shutdown import Shutdowner

class mainFrame():
    def __init__(self):
        """Main form class of the pypoweroff project"""
        self.loader = loadResFile()
        self.options = OptWork()
        self.language = MyLocale()
        self.time = 0
        self.type = False
        self.systype = self.GetSysType()
        self.runed = False
        self.timer_id = None
        self.seconds = None
        self.action = None
        self.hour = None
        self.minutes = None
        self.type_string = None
        self.pofway = False
        self.state = ""
        self.gladefile = ""
        self.isclose = False
        if self.systype == "windows":
            self.gladefile = 'glades\\powoff.glade'
        else:
            self.gladefile = self.loader.get(PROJECT, "glades/powoff.glade")
        if self.gladefile:
            self.widgetTree = Gtk.Builder()
            self.widgetTree.add_from_file(self.gladefile)
        else:
            os.sys.stderr.write("ERROR: No powoff.glade file found")
            os.sys.exit(1)
        dic = {"on_timespin_value_changed": self.ChangeTime, "on_reboot_toggled": self.OnShutdown,
                 "on_shutdown_toggled": self.OnShutdown, "on_timer_id1_toggled": self.SetTimerType,
                 "on_button1_pressed": self.OnButton, "on_exititem_activate": self.OnExit,
                 "on_timer_id2_toggled": self.SetTimerType, "on_hour_spin_value_changed": self.OnHour,
                 "on_min_spin_value_changed": self.OnMinute, "on_ok_button1_pressed": self.OnDialogOk,
                 "on_cancel_button1_pressed": self.OnDialogCancel,
                 "on_aboutitem_activate": self.OnAbout, "on_stopitem_activate": self.OnCancel}
        self.widgetTree.get_objects()
        self.widgetTree.connect_signals(dic)
        self.window = self.widgetTree.get_object('powoff')
        self.delete = self.window.connect("delete-event", self.OnDelete)
        self.window.connect("destroy-event", self.OnDelete)
        self.window.connect("window-state-event", self.OnState)
        self.dialog = self.widgetTree.get_object('def_dialog')
        self.abortitem = self.widgetTree.get_object('stopitem')
        self.button = self.widgetTree.get_object('poffButton')
        #DialogLabels
        self.dialog_label1 = self.widgetTree.get_object('def_dialog_label1')
        self.dialog_label2 = self.widgetTree.get_object('def_dialog_label2')
        #SpinButtons
        timespin = self.widgetTree.get_object('timespin')
        hour_spin = self.widgetTree.get_object('hour_spin')
        min_spin = self.widgetTree.get_object('min_spin')
        #SpinObjects
        self.timeobject = self.widgetTree.get_object('timeto')
        self.hourobject = self.widgetTree.get_object('hours')
        self.minobject = self.widgetTree.get_object('minutes')
        #MainWindowLabels
        window_label1 = self.widgetTree.get_object('label1')
        window_label2 = self.widgetTree.get_object('label3')
        #ToggleButtons
        self.poff_id1 = self.widgetTree.get_object('timer_id1')
        self.poff_id2 = self.widgetTree.get_object('timer_id2')
        self.shut_id1 = self.widgetTree.get_object('shutdown')
        self.shut_id2 = self.widgetTree.get_object('reboot')
        #
        self.sens_objects = (timespin, min_spin, hour_spin, window_label1, window_label2)
        #TrayIcon
        self.trayicon = None
        self.trayicon = StatusIcc(self)
        #Initialize
        self.initLanguage()
        self.InitSettings()
        self.abortitem.set_sensitive(False)
        self.window.show()
#
#==Init Program language
#
    def initLanguage(self):
        self.window.set_title(self.language.main_dic.get('title'))
        self.poff_id1.set_label(self.language.main_dic.get('timerid1'))
        self.poff_id2.set_label(self.language.main_dic.get('timerid2'))
        self.sens_objects[0].set_tooltip_text(self.language.main_dic.get('timespin'))
        self.sens_objects[3].set_text(self.language.main_dic.get('label1'))
        self.sens_objects[4].set_text(self.language.main_dic.get('label3'))
        self.shut_id1.set_label(self.language.main_dic.get('shutdownlabel'))
        self.shut_id1.set_tooltip_text(self.language.main_dic.get('shutdownhint'))
        self.shut_id2.set_label(self.language.main_dic.get('rebootlabel'))
        self.shut_id2.set_tooltip_text(self.language.main_dic.get('reboothint'))
        self.button.set_tooltip_text(self.language.main_dic.get('poffbutton'))
        for item in ['fileitem',  'settingsitem',  'helpitem']:
            if item:
                menu = self.widgetTree.get_object(item)
                menu.set_label(self.language.menu_dic.get(item))

#
#==Work with Settings==
#
    def InitSettings(self):
        self.options.GetSettings()
        timeout = int(self.options.settings.get('timeout'))
        htime = int(self.options.settings.get('htime'))
        mtime = int(self.options.settings.get('mtime'))
        self.sens_objects[0].set_value(timeout)
        self.sens_objects[2].set_value(htime)
        self.sens_objects[1].set_value(mtime)
        self.pofway = bool(self.options.settings.get('pofWay'))
        self.poff_id2.set_active(self.pofway)
        self.poff_id1.set_active(not self.pofway)
        self.SetTimerType(None)
        self.type = bool(self.options.settings.get('typeoff'))
        self.shut_id1.set_active(self.type)
        self.shut_id2.set_active(not self.type)
        self.OnShutdown(None)

    def SaveSettings(self):
        timeout = int(self.timeobject.get_value())
        htime = int(self.hourobject.get_value())
        mtime = int(self.minobject.get_value())
        self.options.SetSettings(0,timeout,int(self.type),htime,mtime,int(self.pofway))
        self.options.WriteConfig()
#
#==Work with Timer==
#
    def OnTimer(self, action):
        if action == 'Start':
            self.seconds = 0
            self.runed = True
            self.trayicon.cancelitem.set_sensitive(True)
            self.abortitem.set_sensitive(True)
            self.button.set_sensitive(False)
            self.timer_id = GObject.timeout_add(1000, self.updateTimer)
        if action == 'Stop':
            if self.timer_id:
                GObject.source_remove(self.timer_id)
                self.timer_id = None
                self.seconds = 0
                self.trayicon.cancelitem.set_sensitive(False)
                self.abortitem.set_sensitive(False)
                self.button.set_sensitive(True)
                self.window.set_title(self.language.main_dic.get('cantitle'))
                self.runed = False

    def updateTimer(self):
        if self.timer_id is not None:
            if self.seconds < self.time:
                self.seconds += 1
                tmpsec = self.language.main_dic.get('tmpsec') + " - " + self.convertTime(self.time - self.seconds)
                self.window.set_title(tmpsec)
                self.trayicon.staticon.set_tooltip_text(tmpsec)
                return True
            else:
                self.Start(self.GetParms())
                self.OnTimer('Stop')
                self.OnDestroy(None)
        else:
            return False
#
#==Work with main window elements==
#
    def ChangeTime(self, widget):
        self.time = widget.get_value()*60

    def OnHour(self, widget):
        self.hour = widget.get_value()

    def OnMinute(self, widget):
        self.minutes = widget.get_value()

    def OnShutdown(self, widget):
        isactive = self.shut_id1.get_active()
        self.type = isactive
        if isactive:
                self.type_string = self.language.dialog_dic.get('typestringsh')
        else:
                self.type_string =  self.language.dialog_dic.get('typestringrb')

    def SetTimerType(self, widget):
        isactive = self.poff_id1.get_active()
        self.sens_objects[0].set_sensitive(isactive) 
        for obj in self.sens_objects[1:]:
             obj.set_sensitive(not isactive) 
        self.pofway = not isactive

    def OnButton(self, widget):
        if not self.runed:
                if self.pofway:
                        self.GetTimeToPoff()
                else:
                        if not self.sens_objects[0].get_value():
                                self.time = 0
                        else:
                                self.time = self.sens_objects[0].get_value()*60
                label1 =  self.language.dialog_dic.get('attentionp1') + " "+self.type_string+" "+  self.language.dialog_dic.get('attentionp2') 
                label2 = self.convertTime(self.time)
                #print(self.time)
                self.RunDialog(label1, label2, 'onRun')
                if self.systype != "windows":
                        shutdown = Shutdowner()
                        label3="Your computer will be"
                        shutdown.Notify(self.loader.get(PROJECT, "images/poweroff.png"), self.language.main_dic.get('tmpsec') +":\n"+label2)
                        del shutdown

    def OnCancel(self, widget):
        self.Stop()

    def OnExit(self, widget):
        label1 = self.language.dialog_dic.get('exitlabel')
        self.RunDialog(label1,'','onExit')
#
#==Work with time==
#
    def convertTime(self, time):
        hour_time = 0
        min_time = 0
        sec_time = 0
        double_null="0"*2
        if time:
            if int(time) > 3599:
                hour_time = int(time/3600)
                min_time = int((time - hour_time*3600)/60)
                sec_time = int(time - hour_time*3600 - min_time*60)
            elif (int(time) > 59) and (int(time) < 3600):
                min_time = int(time/60)
                sec_time = int(time - min_time*60)
            else:
                sec_time = int(time)
            h_time = double_null
            m_time = double_null
            s_time = double_null
            if hour_time < 10:
                h_time = "0"+ str(hour_time)
            else:
                h_time =  str(hour_time)
            if min_time < 10:
                m_time = "0"+ str(min_time)
            else:
                m_time =  str(min_time)
            if sec_time < 10:
                s_time = "0"+ str(sec_time)
            else:
                s_time =  str(sec_time)
            formated = {"H":h_time,"M":m_time,"S":s_time}
            exitTime = "%(H)s : %(M)s : %(S)s" % formated
            return exitTime
        else:
            exitTime = (double_null + " : ")*2 +double_null
            return exitTime

    def GetTimeToPoff(self):
        if self.hourobject.get_value():
            self.hour = self.hourobject.get_value()
        else:
            self.hour = 0
        if self.minobject.get_value():
            self.minutes = self.minobject.get_value()
        else:
            self.minutes = 0
        time_in_seconds = int(self.hour*3600 + self.minutes*60)
        timelist = string.split(time.strftime("%H:%M:%S"), ":")
        currtime = int(int(timelist[0])*3600 + int(timelist[1])*60 + int(timelist[2]))
        if time_in_seconds == currtime:
            self.time = 0
        elif currtime > time_in_seconds:
            self.time = MAX_TIME - (currtime - time_in_seconds)
        elif currtime < time_in_seconds:
            self.time = time_in_seconds - currtime
#
#==Work with dialogs==
#Default dialog
    def RunDialog(self, label1, label2, action):
        if label1:
            self.dialog_label1.set_text(label1)
        if label2:
            self.dialog_label2.set_text(label2)
        else:
            self.dialog_label2.set_text('')
        if action:
            self.action = action
        self.dialog.run()

    def OnDialogOk(self, widget):
        if self.action:
            if self.action == 'onRun':
                if self.time:
                    self.OnTimer('Start')
                    self.dialog.hide()
                else:
                    self.SaveSettings()
                    self.Start(self.GetParms())
                    self.runed = True
                    self.dialog.hide()
            elif self.action == 'onExit':
                if not self.runed:
                    self.SaveSettings()
                    del self.trayicon
                    self.isclose = True
                    self.dialog.destroy()
                    Gtk.main_quit()
                else:
                    self.Stop()
                    self.SaveSettings()
                    del self.trayicon
                    self.isclose = True
                    self.dialog.destroy()
                    Gtk.main_quit()

    def OnDialogCancel(self, widget):
        self.dialog.hide()

#About dialog
    def OnAbout(self, widget):
        about = Gtk.AboutDialog()
        about.set_program_name("pyGTK-PowerOff")
        about.set_version(VERSION)
        about.set_copyright("2009(c) %s (thetvg@gmail.com)"%self.language.main_dic.get('author')) 
        about.set_comments(self.language.main_dic.get('comments'))
        about.set_website("http://sites.google.com/site/thesomeprojects/")
        about.set_website_label(self.language.main_dic.get('website'))
        if self.systype == "windows":
            about.set_logo(GdkPixbuf.Pixbuf.new_from_file("images/poweroff.png"))
        else:
            about.set_logo(GdkPixbuf.Pixbuf.new_from_file(self.loader.get(PROJECT, "images/poweroff.png")))
        about.run()
        about.destroy()
#
#==Other functions==
#
    def GetSysType(self):
        if str(os.sys.platform) == "win32":
            return "windows"
        return "linux"

    def GetParms(self, command=""):
        if self.systype == 'windows':
            if not self.type:
                return "shutdown -r"
            else:
                return "shutdown -s"
        else:
            if not self.type:
                return "reboot"
            else:
                return "shutdown"
        return command

    def MakeAction(self, command):     
        if self.systype == 'windows':
            os.system(command)
            Gtk.main_quit()
        else:
            shutdownder = Shutdowner()
            if command == "reboot":
                shutdownder.Reboot()
            elif command == "shutdown":
                shutdownder.Shutdown()

    def Start(self, command_line):
        self.isclose = True
        if self.systype != 'windows':
            tr1 = threading.Thread(None, self.MakeAction, name="t1", kwargs={"command": command_line})
            tr1.start()
            Gtk.main_quit()
        self.MakeAction(command_line)

    def Stop(self):
        if self.runed:
            self.OnTimer('Stop')
#
#==Work with main window==
#
    def OnDelete(self, window, event):
        if self.isclose:
            return not self.isclose
        self.state = "closed"
        self.OnHide()
        return True

    def OnHide(self):
            if self.window.get_property('visible'):
                self.trayicon.restoreItem.get_children()[0].set_label(self.language.tray_dic.get('restore'))
                self.window.hide()
            else:
                self.trayicon.restoreItem.get_children()[0].set_label(self.language.tray_dic.get('restorehide'))
                if self.state == "iconified":
                    self.window.deiconify()
                    self.window.show_all()
                self.window.show_all()
                self.window.present()
            self.SaveSettings()

    def OnDestroy(self, widget):
        if self.runed:
            self.Stop()
        self.SaveSettings()
        del self.trayicon
        Gtk.main_quit()

    def OnState(self, widget, event):
        if (event.new_window_state == Gdk.WindowState.ICONIFIED) and (event.new_window_state != Gdk.WindowState.WITHDRAWN) :
            self.trayicon.restoreItem.get_children()[0].set_label(self.language.tray_dic.get('restore'))
            self.state = "iconified"
            self.window.hide()
