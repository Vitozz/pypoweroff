#!/usr/bin/env python

from distutils.core import setup
import os

def get_version ():
      f = open("version.txt", "r")
      f.seek(0)
      lines = f.read()
      f.close()
      return "".join(lines).split("\n")[0]

setup(name='pypoweroff',
      version=get_version(),
      description='pyPowerOff package',
      long_description = "Simple python powerroff program written on pyGTK",
      author='Vitaly Tonkacheyev',
      author_email='thetvg@gmail.com',
      url='http://sites.google.com/site/thesomeprojects/',
      maintainer='Vitaly Tonkacheyev',
      maintainer_email='thetvg@gmail.com',
      packages = ['pypoweroff'],
      scripts=['pypoff'],
      data_files=[('/usr/share/applications', ['pypoweroff.desktop']),
                        ('/usr/share/pypoweroff/images', ['images/poweroff.ico']),
                        ('/usr/share/pypoweroff/images', ['images/poweroff.png']),
                        ('/usr/share/pypoweroff/images', ['images/tb_icon.png']),
                        ('/usr/share/pypoweroff/glades', ['glades/powoff.glade']),
                        ('/usr/share/pypoweroff/lang', ['lang/ru.lng']),
                        ('/usr/share/pypoweroff/lang', ['lang/en.lng']),
                        ('/usr/share/pypoweroff/lang', ['lang/ua.lng']),
                    ],
      )
               
