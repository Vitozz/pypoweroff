#!/usr/bin/env python

from distutils.core import setup
from distutils.command.install_data import install_data

setup(name='pypoweroff',
      version='1.2.3',
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
               
