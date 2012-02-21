#-*- coding: utf-8 -*-

import os, threading
from gi.repository import Gtk, GObject, Gdk, GdkPixbuf
import time, string
from .reswork import loadResFile
from .options import OptWork
from .pytrayIcon import StatusIcc
from .pylocale import MyLocale

if str(os.sys.platform) != "win32":
    from .linux_shutdown import Shutdowner

class mainFrame():
    def __init__(self):
        self.__project = "pypoweroff"
        self.loader = loadResFile()
        self.options = OptWork()
        self.language = MyLocale()
        self.time = 0
        self.type = None
        self.systype = self.GetSysType()
        self.runed = False
        self.timer_id = None
        self.seconds = None
        self.action = None
        self.hour = None
        self.minutes = None
        self.type_string = None
        self.pofway = None
        self.state = ""
        self.isclose = False
        self.max_time = int(24*3600)
        if self.systype == "windows":
            self.gladefile = 'glades\\powoff.glade'
        else:
            self.gladefile = self.loader.get(self.__project, "glades/powoff.glade")
        self.widgetTree = Gtk.Builder()
        self.widgetTree.add_from_file(self.gladefile)
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
        #DialogLabels
        self.dialog_label1 = self.widgetTree.get_object('def_dialog_label1')
        self.dialog_label2 = self.widgetTree.get_object('def_dialog_label2')
        #SpinButtons
        self.timespin = self.widgetTree.get_object('timespin')
        self.hour_spin = self.widgetTree.get_object('hour_spin')
        self.min_spin = self.widgetTree.get_object('min_spin')
        #SpinObjects
        self.timeobject = self.widgetTree.get_object('timeto')
        self.hourobject = self.widgetTree.get_object('hours')
        self.minobject = self.widgetTree.get_object('minutes')
        #MainWindowLabels
        self.window_label1 = self.widgetTree.get_object('label1')
        self.window_label2 = self.widgetTree.get_object('label3')
        #ToggleButtons
        self.poff_id1 = self.widgetTree.get_object('timer_id1')
        self.poff_id2 = self.widgetTree.get_object('timer_id2')
        self.shut_id1 = self.widgetTree.get_object('shutdown')
        self.shut_id2 = self.widgetTree.get_object('reboot')
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
        self.timespin.set_tooltip_text(self.language.main_dic.get('timespin'))
        self.window_label1.set_text(self.language.main_dic.get('label1'))
        self.window_label2.set_text(self.language.main_dic.get('label3'))
        self.shut_id1.set_label(self.language.main_dic.get('shutdownlabel'))
        self.shut_id1.set_tooltip_text(self.language.main_dic.get('shutdownhint'))
        self.shut_id2.set_label(self.language.main_dic.get('rebootlabel'))
        self.shut_id2.set_tooltip_text(self.language.main_dic.get('reboothint'))
        button = self.widgetTree.get_object('poffButton')
        button.set_tooltip_text(self.language.main_dic.get('poffbutton'))
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
        self.timespin.set_value(timeout)
        self.hour_spin.set_value(htime)
        self.min_spin.set_value(mtime)
        if self.options.settings.get('pofWay') == 1:
            self.poff_id2.set_active(True)
        elif self.options.settings.get('pofWay') == 0:
            self.poff_id1.set_active(True)
        self.SetTimerType(None)
        if self.options.settings.get('typeoff') == 1:
            self.shut_id1.set_active(True)
        elif self.options.settings.get('typeoff') == 0:
            self.shut_id2.set_active(True)
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
            self.timer_id = GObject.timeout_add(1000, self.updateTimer)
        if action == 'Stop':
            if self.timer_id:
                GObject.source_remove(self.timer_id)
                self.timer_id = None
                self.seconds = 0
                self.trayicon.cancelitem.set_sensitive(False)
                self.abortitem.set_sensitive(False)
                self.window.set_title(self.language.main_dic.get('cantitle'))

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
        if widget.get_value():
            self.time = widget.get_value()*60

    def OnHour(self, widget):
        if widget.get_value():
            self.hour = widget.get_value()

    def OnMinute(self, widget):
        if widget.get_value():
            self.minutes = widget.get_value()

    def OnShutdown(self, widget):
        if self.shut_id1.get_active():
            self.type = 1
            self.type_string = self.language.dialog_dic.get('typestringsh')
        else:
            self.type = 0
            self.type_string =  self.language.dialog_dic.get('typestringrb')

    def SetTimerType(self, widget):
        if self.poff_id1.get_active():
            self.timespin.set_sensitive(True)
            self.hour_spin.set_sensitive(False)
            self.min_spin.set_sensitive(False)
            self.window_label1.set_sensitive(False)
            self.window_label2.set_sensitive(False)
            self.pofway = 0
        else:
            self.timespin.set_sensitive(False)
            self.hour_spin.set_sensitive(True)
            self.min_spin.set_sensitive(True)
            self.window_label1.set_sensitive(True)
            self.window_label2.set_sensitive(True)
            self.pofway = 1

    def OnButton(self, widget):
        if self.pofway > 0:
            self.GetTimeToPoff()
        else:
            if self.timespin.get_value() <= 0:
                self.time = 0
            else:
                self.time = self.timespin.get_value()*60
        label1 =  self.language.dialog_dic.get('attentionp1') + " "+self.type_string+" "+  self.language.dialog_dic.get('attentionp2') 
        label2 = self.convertTime(self.time)
        print(self.time)
        self.RunDialog(label1, label2, 'onRun')

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
        if time>0:
            if int(time) > 3599:
                hour_time = int(time/3600)
                min_time = int((time - hour_time*3600)/60)
                sec_time = int(time - hour_time*3600 - min_time*60)
            elif (int(time) > 59) and (int(time) < 3600):
                min_time = int(time/60)
                sec_time = int(time - min_time*60)
            else:
                sec_time = int(time)
            h_time = "00"
            m_time = "00"
            s_time = "00"
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
            exitTime = "00 : 00 : 00"
            return exitTime

    def GetTimeToPoff(self):
        if self.hourobject.get_value()>0:
            self.hour = self.hourobject.get_value()
        else:
            self.hour = 0
        if self.minobject.get_value()>0:
            self.minutes = self.minobject.get_value()
        else:
            self.minutes = 0
        time_in_seconds = int(self.hour*3600 + self.minutes*60)
        timelist = string.split(time.strftime("%H:%M:%S"), ":")
        currtime = int(int(timelist[0])*3600 + int(timelist[1])*60 + int(timelist[2]))
        if time_in_seconds == currtime:
            self.time = 0
        elif currtime > time_in_seconds:
            self.time = self.max_time - (currtime - time_in_seconds)
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
                if self.time > 0:
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
                    del self.trayicon
                    self.SaveSettings()
                    self.isclose = True
                    self.dialog.destroy()
                    Gtk.main_quit()

    def OnDialogCancel(self, widget):
        self.dialog.hide()

#About dialog
    def OnAbout(self, widget):
        about = Gtk.AboutDialog()
        about.set_program_name("pyGTK-PowerOff")
        about.set_version("1.3.0")
        about.set_copyright("2009(c) %s (thetvg@gmail.com)"%self.language.main_dic.get('author')) 
        about.set_comments(self.language.main_dic.get('comments'))
        about.set_website("http://sites.google.com/site/thesomeprojects/")
        about.set_website_label(self.language.main_dic.get('website'))
        if self.systype == "windows":
            about.set_logo(GdkPixbuf.Pixbuf.new_from_file("images/poweroff.png"))
        else:
            about.set_logo(GdkPixbuf.Pixbuf.new_from_file(self.loader.get(self.__project, "images/poweroff.png")))
        about.run()
        about.destroy()
#
#==Other functions==
#
    def GetSysType(self):
        if str(os.sys.platform) == "win32":
            output = "windows"
        else:
            output = "linux"
        return output

    def GetParms(self, command=""):
        if self.systype == 'windows':
            if self.type == 0:
                command =  "shutdown -r"
            elif self.type == 1:
                command =  "shutdown -s"
        else:
            if self.type == 0:
                command =  "reboot"
            elif self.type == 1:
                command =  "shutdown"
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
        if self.systype != 'windows':
            tr1 = threading.Thread(None, self.MakeAction, name="t1", kwargs={"command": command_line})
            tr1.start()
            self.isclose = True;
            Gtk.main_quit()
        else:
            self.isclose = True;
            self.MakeAction(command_line)

    def Stop(self):
        if self.runed:
            self.OnTimer('Stop')
        else:
            print("Shutdown timer not runned")
#
#==Work with main window==
#
    def OnDelete(self,  window,  event):
        if self.isclose:
            return False
        if self.delete:
            self.state = "closed"
            self.OnHide()
        return True

    def OnHide(self):
            print(self.window.get_property('visible'))
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
        if not self.runed:
            self.SaveSettings()
            del self.trayicon
            Gtk.main_quit()
        else:
            self.Stop()
            del self.trayicon
            self.SaveSettings()
            Gtk.main_quit()

    def OnState(self, widget, event):
        if (event.new_window_state == Gdk.WindowState.ICONIFIED) and (event.new_window_state != Gdk.WindowState.WITHDRAWN) :
            self.trayicon.restoreItem.get_children()[0].set_label(self.language.tray_dic.get('restore'))
            self.state = "iconified"
            self.window.hide()
